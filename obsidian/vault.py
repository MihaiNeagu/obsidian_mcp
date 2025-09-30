"""
Obsidian Vault interaction class
"""

import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ObsidianVault:
    """Handles interactions with an Obsidian vault"""

    def __init__(self, vault_path: Optional[str] = None):
        self.vault_path = Path(vault_path) if vault_path else Path.home() / "Documents" / "Obsidian"
        if not self.vault_path.exists():
            self.vault_path.mkdir(parents=True, exist_ok=True)

    def list_notes(self, folder: Optional[str] = None) -> List[Dict[str, str]]:
        """List all markdown files in the vault or specific folder"""
        search_path = self.vault_path / folder if folder else self.vault_path
        notes = []

        if search_path.exists():
            for file_path in search_path.rglob("*.md"):
                relative_path = file_path.relative_to(self.vault_path)
                notes.append({
                    "name": file_path.stem,
                    "path": str(relative_path),
                    "full_path": str(file_path),
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })

        return notes

    def read_note(self, note_path: str) -> Optional[str]:
        """Read the content of a specific note"""
        file_path = self.vault_path / note_path
        if file_path.exists() and file_path.suffix == ".md":
            return file_path.read_text(encoding='utf-8')
        return None

    def write_note(self, note_path: str, content: str) -> bool:
        """Write or update a note"""
        file_path = self.vault_path / note_path

        # Ensure the file has .md extension
        if not file_path.suffix:
            file_path = file_path.with_suffix('.md')

        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            file_path.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            logger.error(f"Failed to write note: {e}")
            return False

    def delete_note(self, note_path: str) -> bool:
        """Delete a note from the vault"""
        file_path = self.vault_path / note_path
        if file_path.exists() and file_path.suffix == ".md":
            try:
                file_path.unlink()
                return True
            except Exception as e:
                logger.error(f"Failed to delete note: {e}")
                return False
        return False

    def search_notes(self, query: str) -> List[Dict[str, Any]]:
        """Search for notes containing the query string"""
        results = []
        query_lower = query.lower()

        for file_path in self.vault_path.rglob("*.md"):
            try:
                content = file_path.read_text(encoding='utf-8')
                if query_lower in content.lower():
                    relative_path = file_path.relative_to(self.vault_path)
                    # Find matching lines
                    lines = content.split('\n')
                    matching_lines = []
                    for i, line in enumerate(lines):
                        if query_lower in line.lower():
                            matching_lines.append({
                                "line_number": i + 1,
                                "content": line.strip()[:100]  # First 100 chars
                            })

                    results.append({
                        "name": file_path.stem,
                        "path": str(relative_path),
                        "matches": matching_lines[:5]  # Limit to first 5 matches
                    })
            except Exception as e:
                logger.error(f"Error searching file {file_path}: {e}")

        return results

    def get_note_metadata(self, note_path: str) -> Optional[Dict[str, Any]]:
        """Extract frontmatter metadata from a note"""
        content = self.read_note(note_path)
        if not content:
            return None

        lines = content.split('\n')
        if lines and lines[0].strip() == '---':
            # Find the closing ---
            metadata_lines = []
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    break
                metadata_lines.append(line)

            if metadata_lines:
                try:
                    import yaml
                    metadata_str = '\n'.join(metadata_lines)
                    return yaml.safe_load(metadata_str)
                except:
                    # If yaml parsing fails, return raw lines
                    return {"raw": metadata_lines}

        return {}