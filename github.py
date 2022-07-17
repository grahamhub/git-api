import logging
import os
import requests
from logging import Logger

class Github:
    GITHUB_PAT = os.environ.get("GITHUB_PAT", "")
    LOGGER = Logger("github")
    BASE_URL = "https://api.github.com"
    OWNER = "grahamhub"

    def _build_request(self, method, url, content_type, payload=None):
        headers = {
            "Authorization": f"token {self.GITHUB_PAT}",
            "Accept": f"application/vnd.github+{content_type}",
        }

        try:
            r = requests.request(method, url, json=payload, headers=headers)
            return r.json()
        except requests.HTTPError as e:
            self.LOGGER.info(e)
            return {"message": "exception occurred, check logs"}
    
    def get_ref(self, repo, ref):
        resp = self._build_request(
            "GET",
            f"{self.BASE_URL}/repos/{self.OWNER}/{repo}/git/ref/{ref}",
            "json",
        )

        return resp.get("object", resp)
    
    def create_ref(self, repo, sha, ref):
        resp = self._build_request(
            "POST",
            f"{self.BASE_URL}/repos/{self.OWNER}/{repo}/git/refs",
            "json",
            {"sha":sha, "ref":ref},
        )

        return resp.get("object", resp)
    
    def update_ref(self, repo, sha, ref):
        resp = self._build_request(
            "PATCH",
            f"{self.BASE_URL}/repos/{self.OWNER}/{repo}/git/refs/{ref}",
            "json",
            {"sha":sha}
        )

        return resp.get("object", resp)
    
    def get_blob(self, repo, sha):
        resp = self._build_request(
            "GET",
            f"{self.BASE_URL}/repos/{self.OWNER}/{repo}/git/blobs/{sha}",
            "json",
        )

        return resp
    
    def create_blob(self, repo, content, encoding):
        resp = self._build_request(
            "POST",
            f"{self.BASE_URL}/repos/{self.OWNER}/{repo}/git/blobs",
            "json",
            {"content":content, "encoding":encoding}
        )

        return resp.get("sha", resp)
    
    def get_commit(self, repo, sha):
        resp = self._build_request(
            "GET",
            f"{self.BASE_URL}/repos/{self.OWNER}/{repo}/git/commits/{sha}",
            "json",
        )

        commit = {
            "sha": resp.get("sha", False),
            "message": resp.get("message", False),
            "html_url": resp.get("html_url", False),
        }

        if not commit.get("sha"):
            return resp
        
        return commit
    
    def create_commit(self, repo, message, tree, parents=[]):
        resp = self._build_request(
            "POST",
            f"{self.BASE_URL}/repos/{self.OWNER}/{repo}/git/commits",
            "json",
            {"message": message, "tree": tree, "parents": parents},
        )

        commit = {
            "sha": resp.get("sha", False),
            "message": resp.get("message", False),
            "html_url": resp.get("html_url", False),
        }

        if not commit.get("sha"):
            return resp
        
        return commit
    
    def get_tree(self, repo, sha):
        resp = self._build_request(
            "GET",
            f"{self.BASE_URL}/repos/{self.OWNER}/{repo}/git/trees/{sha}",
            "json",
        )

        return resp
    
    def create_tree(self, repo, base_tree, tree):
        resp = self._build_request(
            "POST",
            f"{self.BASE_URL}/repos/{self.OWNER}/{repo}/git/trees",
            "json",
            {"base_tree": base_tree, "tree": tree},
        )

        return resp
    
    def merge(self, repo, base, head, message):
        resp = self._build_request(
            "POST",
            f"{self.BASE_URL}/repos/{self.OWNER}/{repo}/merges",
            "json",
            {"base":base, "head":head, "commit_message":message},
        )

        return resp
