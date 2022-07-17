from exceptions import NoApiTokenException
import models
import os

from exceptions import NoApiTokenException
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from github import Github

app = FastAPI()
gh = Github()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_key = os.environ.get("GIT_API_TOKEN", False)

if not api_key:
    raise NoApiTokenException

def api_key_auth(recv_api_key=Depends(oauth2_scheme)):
    if recv_api_key != api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


@app.get("/", dependencies=[Depends(api_key_auth)])
def read_root():
    return {"status": "ok"}


@app.get("/branch/{branch_name}", dependencies=[Depends(api_key_auth)])
def get_branch(branch_name, repo):
    ref = gh.get_ref(repo, f"heads/{branch_name}")
    sha = ref.get("sha", False)

    if not sha:
        return ref

    return {"sha": ref.get("sha", "")}


@app.post("/branch/new", dependencies=[Depends(api_key_auth)])
def create_branch(branch: models.CreateBranchInput):
    new_ref = gh.create_ref(branch.repo, branch.sha, branch.ref)
    sha = new_ref.get("sha", False)

    if not sha:
        return new_ref
    
    return {"sha": new_ref.get("sha", "")}


@app.patch("/branch/{branch_name}", dependencies=[Depends(api_key_auth)])
def update_branch(branch_name, branch: models.UpdateBranchInput):
    new_ref = gh.update_ref(branch.repo, branch.sha, f"heads/{branch_name}")
    sha = new_ref.get("sha", False)

    if not sha:
        return new_ref
    
    return {"sha": new_ref.get("sha", "")}


@app.get("/blobs/{sha}", dependencies=[Depends(api_key_auth)])
def get_blob(sha, repo):
    blob = gh.get_blob(repo, sha)
    return blob


@app.post("/blobs/new", dependencies=[Depends(api_key_auth)])
def create_blob(blob: models.CreateBlobInput):
    sha = gh.create_blob(blob.repo, blob.content, blob.encoding)
    return {"sha": sha}


@app.get("/commits/{sha}", dependencies=[Depends(api_key_auth)])
def get_commit(sha, repo):
    commit = gh.get_commit(repo, sha)
    return commit


@app.post("/commits/new", dependencies=[Depends(api_key_auth)])
def create_commit(commit: models.CreateCommitInput):
    new_commit = gh.create_commit(
        commit.repo,  commit.message, commit.tree, commit.parents
    )
    return new_commit


@app.get("/trees/{sha}", dependencies=[Depends(api_key_auth)])
def get_tree(sha, repo):
    tree = gh.get_tree(repo, sha)
    return tree


@app.post("/trees/new", dependencies=[Depends(api_key_auth)])
def create_tree(tree: models.CreateTreeInput):
    new_tree = gh.create_tree(tree.repo, tree.base_tree, tree.tree)
    return new_tree


@app.post("/merge", dependencies=[Depends(api_key_auth)])
def merge(merge: models.MergeInput):
    merged = gh.merge(merge.repo, merge.base, merge.head, merge.message)
    return merged
