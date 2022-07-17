from pydantic import BaseModel

class CreateBranchInput(BaseModel):
    repo: str
    ref: str
    sha: str


class UpdateBranchInput(BaseModel):
    repo: str
    sha: str


class CreateBlobInput(BaseModel):
    repo: str
    content: str
    encoding: str


class CreateCommitInput(BaseModel):
    repo: str
    message: str
    tree: str
    parents: list[str]


class Tree(BaseModel):
    path: str
    mode: str
    type: str
    sha: str


class CreateTreeInput(BaseModel):
    repo: str
    base_tree: str
    tree: list


class MergeInput(BaseModel):
    repo: str
    base: str
    head: str
    message: str
