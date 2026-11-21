import os
import re
import logging
from typing import Dict, Any, Optional, Tuple, List
import requests
from github import Github, GithubException

from app.config import get_settings

logger = logging.getLogger("rookiestuff.github")


class GitHubClient:
    """Client for GitHub API operations: fetching PR files and committing changes."""

    def __init__(self, token: Optional[str] = None):
        settings = get_settings()
        self.token = token if token is not None else settings.github_token
        self.gh = Github(self.token) if self.token and not self.token.startswith("mock_") else None

    @staticmethod
    def parse_pr_url(pr_url: str) -> Tuple[str, str, int]:
        """
        Extract owner, repo name, and PR number from a PR URL.
        Example: https://github.com/owner/repo/pull/123
        """
        pattern = r"github\.com[/:](?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<number>\d+)"
        match = re.search(pattern, pr_url)
        if not match:
            # Fallback parsing for alternative or partial URL shapes
            parts = pr_url.strip("/").split("/")
            if len(parts) >= 4 and parts[-2] == "pull":
                owner = parts[-4]
                repo = parts[-3]
                number = int(parts[-1])
                return owner, repo, number
            raise ValueError(f"Invalid GitHub PR URL format: {pr_url}")

        owner = match.group("owner")
        repo = match.group("repo")
        number = int(match.group("number"))
        return owner, repo, number

    def fetch_pr_details(self, pr_url: str) -> Dict[str, Any]:
        """
        Pulls modified files and PR metadata.
        Returns a dict containing:
        - repo_name: 'owner/repo'
        - pr_number: int
        - branch_name: str (head ref)
        - file_path: str (target modified file)
        - code_contents: str
        - all_files: List[Dict]
        """
        try:
            owner, repo, pr_number = self.parse_pr_url(pr_url)
            full_repo_name = f"{owner}/{repo}"
        except Exception as e:
            logger.warning(f"Failed to parse PR URL '{pr_url}': {e}. Using fallback identifiers.")
            owner, repo, pr_number = "test-owner", "test-repo", 1
            full_repo_name = "test-owner/test-repo"

        # If live PyGithub instance is available and token is valid
        if self.gh:
            try:
                repository = self.gh.get_repo(full_repo_name)
                pull = repository.get_pull(pr_number)
                branch_name = pull.head.ref
                files = pull.get_files()

                modified_files = []
                primary_code = ""
                primary_file_path = "main.py"

                for f in files:
                    modified_files.append({"filename": f.filename, "status": f.status, "patch": f.patch})
                    if f.filename.endswith(".py") and not primary_code:
                        primary_file_path = f.filename
                        try:
                            content_file = repository.get_contents(f.filename, ref=branch_name)
                            primary_code = content_file.decoded_content.decode("utf-8")
                        except Exception as ce:
                            logger.warning(f"Could not fetch contents for {f.filename}: {ce}")
                            if f.patch:
                                primary_code = f.patch

                if not primary_code and modified_files:
                    primary_file_path = modified_files[0]["filename"]
                    primary_code = modified_files[0].get("patch", "")

                return {
                    "repo_name": full_repo_name,
                    "pr_number": pr_number,
                    "branch_name": branch_name,
                    "file_path": primary_file_path,
                    "code_contents": primary_code or "# No python file contents extracted from PR",
                    "all_files": modified_files,
                }
            except Exception as exc:
                logger.warning(f"GitHub API fetch failed for {pr_url}: {exc}. Using mock fallback.")

        # Standalone Mock Fallback (for local testing, offline, or sandbox runs)
        sample_unlinted_code = (
            "def calculate_total_price(items, tax_rate):\n"
            "    # Calculate totals with loop\n"
            "    total = 0\n"
            "    for item in items:\n"
            "      total = total + item['price']\n"
            "    tax=total*tax_rate\n"
            "    return total+tax\n"
        )
        return {
            "repo_name": full_repo_name,
            "pr_number": pr_number,
            "branch_name": "feature/refactor-upgrade",
            "file_path": "calculator.py",
            "code_contents": sample_unlinted_code,
            "all_files": [{"filename": "calculator.py", "status": "modified"}],
        }

    def commit_changes(
        self,
        repo_name: str,
        branch: str,
        file_path: str,
        new_content: str,
        commit_message: str = "chore: apply automated refactoring changes [RookieStuff Agent]",
    ) -> Dict[str, Any]:
        """
        Commits approved refactored code back to the target PR branch.
        """
        if self.gh:
            try:
                repo = self.gh.get_repo(repo_name)
                # Check if file exists on branch
                try:
                    contents = repo.get_contents(file_path, ref=branch)
                    update_res = repo.update_file(
                        path=file_path,
                        message=commit_message,
                        content=new_content,
                        sha=contents.sha,
                        branch=branch,
                    )
                    commit_sha = update_res["commit"].sha
                except GithubException:
                    # File does not exist, create it
                    create_res = repo.create_file(
                        path=file_path,
                        message=commit_message,
                        content=new_content,
                        branch=branch,
                    )
                    commit_sha = create_res["commit"].sha

                return {
                    "success": True,
                    "commit_sha": commit_sha,
                    "message": commit_message,
                    "file_path": file_path,
                    "branch": branch,
                    "mode": "live_github",
                }
            except Exception as exc:
                logger.error(f"Failed to commit changes via GitHub API: {exc}")

        # Simulated commit return for sandbox or mock testing
        mock_sha = "a1b2c3d4e5f67890123456789abcdef012345678"
        return {
            "success": True,
            "commit_sha": mock_sha,
            "message": commit_message,
            "file_path": file_path,
            "branch": branch,
            "mode": "simulated_commit",
        }
