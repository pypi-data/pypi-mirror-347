"""Command-line interface for **ONNXNPU Toolkit**.

After installing the package, this module is exposed as the console-scripts
`onpu` and `onnxnpu` (configured in pyproject.toml).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List
import onnx

from . import __version__
from .checker import (
    Checker,
    iter_profiles,
    load_profile,
    print_model_summary,
    print_summary,
    valid_check,
)
from .optimizer import update_opset_version

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    """Build the main argument parser with subcommands."""
    # Main parser
    parser = argparse.ArgumentParser(
        prog="onpu",
        description="ONNXNPU Toolkit - Check, optimize and modify ONNX models for NPU deployment",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"{__version__}",
        help="Show version number and exit"
    )
    
    # Create subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Check command
    check_parser = subparsers.add_parser(
        "check", 
        help="Check ONNX model compatibility with NPU hardware profiles",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    check_parser.add_argument("model", help="Path to .onnx model file")
    check_parser.add_argument(
        "-p",
        "--hardware",
        nargs="*",
        help="Profile name(s) (e.g. kl720) or JSON file path(s). Omit to scan all built-in profiles.",
    )
    check_parser.add_argument("--markdown", action="store_true", help="Output report(s) as Markdown")
    
    # Opt command
    
    opt_parser = subparsers.add_parser(
        "opt", 
        help="Optimize and modify ONNX models",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    opt_parser.add_argument("model", help="Path to .onnx model file")
    opt_parser.add_argument(
        "-o", "--output",
        help="Output path for optimized model",
    )
    
    # Optimization options
    opt_parser.add_argument(
        "--opset", 
        type=int,
        help="Update model to specified opset version (12-18)",
        metavar="VERSION",
        choices=range(12, 18),  # Max version 18 as specified
    )
    opt_parser.add_argument(
        "--skip-check", 
        action="store_true",
        help="Skip correctness checking after simplification"
    )
    opt_parser.add_argument(
        "--overwrite-shapes", 
        action="store_true",
        help="Allow overwriting input shapes during optimization"
    )
    opt_parser.add_argument(
        "--skip-optimizers",
        nargs="+",
        help="List of optimizers to skip during simplification"
    )
    opt_parser.add_argument(
        "-p",
        "--hardware",
        nargs="*",
        help="Profile name(s) (e.g. kl720) for checking compatibility after optimization."
    )
    
    # List command
    list_parser = subparsers.add_parser(
        "list",
        help="List available hardware profiles",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    list_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed information about each profile"
    )
    
    return parser

# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def check_command(args) -> None:
    """Handle the 'check' subcommand."""
    model_path = Path(args.model)
    
    valid_check(model_path)
    
    # Show model IO + detect dynamic axes
    dynamic = print_model_summary(model_path)
    
    # Determine which profiles to scan
    profile_keys = args.hardware if args.hardware else iter_profiles()
    
    for key in profile_keys:
        profile = load_profile(key)
        
        # Warn if KL* profile & dynamic dims present
        if dynamic and profile.get("name", "").lower().startswith("kl"):
            print(f"[WARNING] Model uses dynamic axes which are NOT supported on {profile['name']}.")
        
        # Create checker with skip_size_check option
        checker = Checker(model_path, profile)
        report = checker.run()
        
        print(report.to_markdown() if args.markdown else report)
        print_summary(report)
        print()

def opt_command(args) -> None:
    """Handle the 'opt' subcommand."""
    model_path = Path(args.model)
    output_path = Path(args.output) if args.output else None
    
    # Validate original model first
    try:
        valid_check(model_path)
    except Exception as e:
        print(f"WARNING: Input model validation failed: {str(e)}")
        print("Attempting to optimize despite validation issues...")
    
    # Apply model optimization with optional opset update
    from .optimizer import optimize_model
    
    hardware_profile = None
    if hasattr(args, 'hardware') and args.hardware:
        hardware_profile = args.hardware[0]
    
    check_n = 0 if args.skip_check else 1
    
    final_path, success = optimize_model(
        model_path=model_path,
        output_path=output_path,
        check_n=check_n,
        overwrite_input_shapes=args.overwrite_shapes,
        skip_optimizers=args.skip_optimizers,
        target_opset=args.opset,  # Pass opset directly to the optimize function
        hardware_profile=hardware_profile,
        )
    
    # Print model summary of final optimized model if no hardware profile was specified
    # (otherwise the check was done inside optimize_model)
    if not hardware_profile:
        print_model_summary(final_path)
        
def list_command(args) -> None:
    """Handle the 'list' subcommand."""
    profile_names = iter_profiles()
    
    if not profile_names:
        print("No hardware profiles found.")
        return
    
    print(f"Available hardware profiles ({len(profile_names)}):")
    print("-" * 50)
    
    if args.verbose:
        # Detailed view with description and supported op count
        for name in profile_names:
            try:
                profile = load_profile(name)
                description = profile.get("description", "No description available")
                op_count = len(profile.get("operators", {}))
                print(f"{name.upper()}: {description}")
                print(f"  Supported operators: {op_count}")
                print()
            except Exception as e:
                print(f"{name.upper()}: Error loading profile - {str(e)}")
                print()
    else:
        # Simple list view
        for i, name in enumerate(profile_names, 1):
            print(f"{i}. {name.upper()}")

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main(argv: List[str] | None = None) -> None:
    args = _build_parser().parse_args(argv)
    
    # Handle legacy command style (no subcommand)
    if args.command is None:
        # If the first argument looks like a file path, assume it's the 'check' command
        if len(sys.argv) > 1 and not sys.argv[1].startswith('-') and Path(sys.argv[1]).exists():
            print("[DEPRECATED] Running in legacy mode. Please use 'onpu check' instead.")
            # Reconstruct arguments as if 'check' was specified
            if argv is None:
                argv = sys.argv[1:]
            else:
                argv = ['check'] + argv
            args = _build_parser().parse_args(argv)
        else:
            print("Error: No command specified. Use 'check' or 'opt'.")
            _build_parser().print_help()
            return
    
    # Dispatch to appropriate command handler
    if args.command == "check":
        check_command(args)
    elif args.command == "opt":
        opt_command(args)
    elif args.command == "list":
        list_command(args)

if __name__ == "__main__":  # pragma: no cover
    main()