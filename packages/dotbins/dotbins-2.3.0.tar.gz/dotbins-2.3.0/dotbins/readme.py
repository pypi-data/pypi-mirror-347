"""README generation utilities for dotbins."""

from __future__ import annotations

import datetime
import math
from typing import TYPE_CHECKING, Any, NamedTuple

from rich.console import Console
from rich.markdown import Markdown

from dotbins import __version__

from .utils import current_platform, log, replace_home_in_path, tag_to_version

if TYPE_CHECKING:
    from pathlib import Path

    from .config import Config


class _ToolData(NamedTuple):
    """Container for tool data gathered for README generation."""

    tools_info: dict[str, dict[str, Any]]
    total_tools: int
    total_size_bytes: int
    tool_sizes: dict[str, int]
    arch_counts: dict[str, int]
    counted_archs: set[tuple[str, str, str]]


def _format_size(size_bytes: float) -> str:
    """Format size in bytes to a human readable string."""
    if size_bytes == 0:
        return "0 B"

    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = math.floor(math.log(size_bytes, 1024))
    # Handle potential out of range index
    i = min(i, len(size_names) - 1)
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"


def _format_timestamp(timestamp: str) -> str:
    """Format ISO timestamp to a more readable format."""
    # Handle empty timestamps
    if not timestamp or timestamp == "Unknown":
        return timestamp  # pragma: no cover

    try:
        dt = datetime.datetime.fromisoformat(timestamp)
        return dt.strftime("%b %d, %Y")
    except (ValueError, TypeError):  # pragma: no cover
        return timestamp


def _gather_tool_data(config: Config) -> _ToolData:
    """Gather data about all tools managed by dotbins.

    Returns:
        ToolData containing:
        - tools_info: Dictionary of tool information
        - total_tools: Number of installed tools
        - total_size_bytes: Total size of all binaries
        - tool_sizes: Dictionary of tool sizes
        - arch_counts: Dictionary counting architectures per tool
        - counted_archs: Set of (tool, platform, arch) tuples already counted

    """
    tools = sorted(config.tools.keys())

    total_tools = 0
    total_size_bytes = 0
    tool_sizes: dict[str, int] = {}
    tool_arch_counts: dict[str, int] = {}
    arch_counted: set[tuple[str, str, str]] = set()
    tool_data: dict[str, dict[str, Any]] = {}

    for tool_name in tools:
        tool_config = config.tools[tool_name]
        repo = tool_config.repo
        repo_url = f"https://github.com/{repo}"

        # Create entry for this tool if it doesn't exist
        if tool_name not in tool_data:
            tool_data[tool_name] = {"repo": repo, "repo_url": repo_url, "platforms": {}}

        # Add data for each platform/architecture combination
        for platform, architectures in config.platforms.items():
            if platform not in tool_data[tool_name]["platforms"]:
                tool_data[tool_name]["platforms"][platform] = {}

            for arch in architectures:
                tool_info = config.manifest.get_tool_info(tool_name, platform, arch)
                if tool_info:
                    tag = tool_info.get("tag", "Unknown")
                    updated_at = tool_info.get("updated_at", "Unknown")
                    updated_at = _format_timestamp(updated_at)

                    current_platform_name, current_arch_name = current_platform()
                    is_current = platform == current_platform_name and arch == current_arch_name
                    current_marker = " ***(current)***" if is_current else ""

                    tool_data[tool_name]["platforms"][platform][arch] = {
                        "tag": tag,
                        "updated_at": updated_at,
                        "is_current": is_current,
                        "current_marker": current_marker,
                    }

                    # Calculate file sizes for statistics
                    bin_dir = config.bin_dir(platform, arch)
                    if bin_dir.exists():
                        # Initialize tool counters if this is the first time we see this tool
                        if tool_name not in tool_sizes:
                            tool_sizes[tool_name] = 0
                            tool_arch_counts[tool_name] = 0

                        # Count unique architecture per tool only once
                        arch_tuple = (tool_name, platform, arch)
                        if arch_tuple not in arch_counted:
                            arch_counted.add(arch_tuple)
                            tool_arch_counts[tool_name] += 1

                        # Add sizes for all binaries
                        for binary_name in tool_config.binary_name:
                            binary_path = bin_dir / binary_name
                            # add .exe on Windows
                            if current_platform_name == "windows":  # pragma: no cover
                                binary_path = binary_path.with_suffix(".exe")
                            if binary_path.exists():
                                size = binary_path.stat().st_size
                                total_size_bytes += size
                                tool_sizes[tool_name] += size

                    total_tools += 1

    return _ToolData(
        tools_info=tool_data,
        total_tools=total_tools,
        total_size_bytes=total_size_bytes,
        tool_sizes=tool_sizes,
        arch_counts=tool_arch_counts,
        counted_archs=arch_counted,
    )


def _generate_tool_table(tool_data: dict[str, dict[str, Any]]) -> list[str]:
    """Generate the tool table markdown content."""
    content = [
        "## 🔍 Installed Tools",
        "",
        "| Tool | Repository | Version | Updated | Platforms & Architectures |",
        "| :--- | :--------- | :------ | :------ | :------------------------ |",
    ]

    for tool_name, data in tool_data.items():
        repo = data["repo"]
        repo_url = data["repo_url"]

        architectures_by_platform: dict[str, str] = {}
        for platform, archs in data["platforms"].items():
            arch_info: list[str] = list(archs)
            if arch_info:
                architectures_by_platform[platform] = ", ".join(arch_info)

        tag = "Not installed"
        updated_at = "N/A"
        for archs in data["platforms"].values():
            for info in archs.values():
                tag = info["tag"]
                updated_at = info["updated_at"]
                break
            if tag != "Not installed":
                break

        platform_arch_list: list[str] = []
        for platform, archs_str in architectures_by_platform.items():
            platform_arch_list.append(f"{platform} ({archs_str})")

        platforms_str = " • ".join(platform_arch_list)

        if platforms_str:
            version = tag_to_version(tag)
            content.append(
                f"| [{tool_name}]({repo_url}) | {repo} | {version} | {updated_at} | {platforms_str} |",
            )

    return content


def _generate_stats_table(
    total_tools: int,
    total_size_bytes: int,
    tool_sizes: dict[str, int],
    tool_arch_counts: dict[str, int],
) -> list[str]:
    """Generate statistics table content."""
    content = [
        "## 📊 Tool Statistics",
        "",
        f"<div align='center'><h3>📦 {total_tools} Tools | 💾 {_format_size(total_size_bytes)} Total Size</h3></div>",
        "",
        "| Tool | Total Size | Avg Size per Architecture |",
        "| :--- | :-------- | :------------------------ |",
    ]

    for tool_name, size in sorted(tool_sizes.items(), key=lambda x: x[1], reverse=True):
        arch_count = tool_arch_counts[tool_name]
        avg_size = size / arch_count if arch_count > 0 else size
        content.append(f"| {tool_name} | {_format_size(size)} | {_format_size(avg_size)} |")

    return content


def _generate_shell_integration(tools_dir: Path) -> list[str]:
    """Generate shell integration section content."""
    tools_dir_str = replace_home_in_path(tools_dir)
    return [
        "## 💻 Shell Integration",
        "",
        "Add one of the following snippets to your shell configuration file to use the platform-specific binaries:",
        "",
        "For **Bash**:",
        "```bash",
        f"source {tools_dir_str}/shell/bash.sh",
        "```",
        "",
        "For **Zsh**:",
        "```bash",
        f"source {tools_dir_str}/shell/zsh.sh",
        "```",
        "",
        "For **Fish**:",
        "```fish",
        f"source {tools_dir_str}/shell/fish.fish",
        "```",
        "",
        "For **Nushell**:",
        "```nu",
        f"source {tools_dir_str}/shell/nushell.nu",
        "```",
    ]


def _generate_updating_section() -> list[str]:
    """Generate section content for installing and updating tools."""
    return [
        "## 🔄 Installing and Updating Tools",
        "",
        "### Install or update all tools",
        "```bash",
        "dotbins sync",
        "```",
        "",
        "### Install or update specific tools only",
        "```bash",
        "dotbins sync tool1 tool2",
        "```",
        "",
        "### Install or update for current platform only",
        "```bash",
        "dotbins sync --current",
        "```",
        "",
        "### Force reinstall of all tools",
        "```bash",
        "dotbins sync --force",
        "```",
        "",
    ]


def _generate_commands_section() -> list[str]:
    """Generate quick commands section content."""
    return [
        "## 🚀 Quick Commands",
        "",
        "<details>",
        "<summary>All available commands</summary>",
        "",
        "```",
        "dotbins list           # List all available tools",
        "dotbins init           # Initialize directory structure",
        "dotbins sync           # Install and update tools to their latest versions",
        "dotbins readme         # Regenerate this README",
        "dotbins status         # Show installed tool versions",
        "dotbins get REPO       # Install tool directly to ~/.local/bin",
        "```",
        "",
        "For detailed usage information, run `dotbins --help` or `dotbins <command> --help`",
        "</details>",
    ]


def _generate_config_section(config: Config) -> list[str]:
    """Generate section showing the configuration file content."""
    content = [
        "## 📁 Configuration File",
        "",
        "dotbins is configured using a YAML file (`dotbins.yaml`).",
        "This configuration defines which tools to manage, their sources, and platform compatibility.",
        "",
        "**Current Configuration:**",
        "",
        "```yaml",
    ]

    config_content = ""
    if config.config_path:
        try:
            config_content = config.config_path.read_text().strip()
        except OSError:  # pragma: no cover
            config_content = "# Error reading configuration file"

    if not config_content:
        config_content = "# Configuration file not found"

    content.extend([config_content, "```"])
    return content


def _generate_additional_info() -> list[str]:
    """Generate additional information section content."""
    platform_info = current_platform()
    current_platform_name, current_arch_name = platform_info

    return [
        "## ℹ️ Additional Information",  # noqa: RUF001
        "",
        f"* This README was automatically generated on {datetime.datetime.now().strftime('%b %d, %Y')}",
        f"* Current platform: **{current_platform_name}/{current_arch_name}**",
        "* For more information on dotbins, visit https://github.com/basnijholt/dotbins",
    ]


def generate_readme_content(config: Config) -> str:
    """Generate a markdown README file for the tools directory."""
    # Gather tool information and statistics
    data = _gather_tool_data(config)

    # Build content sections
    content: list[str] = [
        "# 🛠️ dotbins Tool Collection",
        "",
        f"[![dotbins](https://img.shields.io/badge/powered%20by-dotbins-blue.svg?style=flat-square)](https://github.com/basnijholt/dotbins) [![Version](https://img.shields.io/badge/version-{__version__}-green.svg?style=flat-square)](https://github.com/basnijholt/dotbins/releases)",
        "",
        "This directory contains command-line tools automatically managed by [dotbins](https://github.com/basnijholt/dotbins).",
        "",
        "## 📋 Table of Contents",
        "",
        "- [What is dotbins?](#-what-is-dotbins)",
        "- [Installed Tools](#-installed-tools)",
        "- [Tool Statistics](#-tool-statistics)",
        "- [Shell Integration](#-shell-integration)",
        "- [Installing and Updating Tools](#-installing-and-updating-tools)",
        "- [Quick Commands](#-quick-commands)",
        "- [Configuration File](#-configuration-file)",
        "- [Additional Information](#ℹ️-additional-information)",  # noqa: RUF001
        "",
        "## 📦 What is dotbins?",
        "",
        "**dotbins** is a utility for managing CLI tool binaries in your dotfiles repository."
        " It downloads and organizes binaries for popular command-line tools across multiple platforms"
        " (macOS, Linux) and architectures (amd64, arm64).",
        "",
        "**Key features:**",
        "",
        "- ✅ **Cross-platform support** - Manages tools for different OSes and CPU architectures",
        "- ✅ **No admin privileges** - Perfect for systems where you lack sudo access",
        "- ✅ **Version tracking** - Keeps track of installed tools with update timestamps",
        "- ✅ **GitHub integration** - Automatically downloads from GitHub releases",
        "- ✅ **Simple configuration** - YAML-based config with auto-detection capabilities",
        "",
        "Learn more: [github.com/basnijholt/dotbins](https://github.com/basnijholt/dotbins)",
        "",
    ]

    # Generate and add each section
    content.extend(_generate_tool_table(data.tools_info))
    content.append("")
    content.extend(
        _generate_stats_table(
            data.total_tools,
            data.total_size_bytes,
            data.tool_sizes,
            data.arch_counts,
        ),
    )
    content.append("")
    content.extend(_generate_shell_integration(config.tools_dir))
    content.append("")
    content.extend(_generate_updating_section())
    content.append("")
    content.extend(_generate_commands_section())
    content.append("")
    content.extend(_generate_config_section(config))
    content.append("")
    content.extend(_generate_additional_info())

    # Convert all content items to strings (important for tests with MagicMock objects)
    content = [str(item) for item in content]
    return "\n".join(content)


def write_readme_file(
    config: Config,
    write_file: bool = True,
    print_content: bool = False,
    verbose: bool = False,
) -> None:
    """Generate and write a README.md file to the tools directory."""
    readme_content = generate_readme_content(config)
    readme_path = config.tools_dir / "README.md"

    if write_file:
        try:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(readme_content)
            readme_path_str = replace_home_in_path(readme_path, "~")
            log(f"Generated README at {readme_path_str}", "success", "📝")
        except OSError as e:
            log(f"Failed to write README: {e}", "error", print_exception=verbose)
        except Exception as e:  # pragma: no cover
            log(f"Unexpected error writing README: {e}", "error", print_exception=verbose)

    if print_content:
        console = Console()
        md = Markdown(readme_content)
        console.print(md)
