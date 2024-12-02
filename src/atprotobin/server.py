import os
import hashlib
import pathlib
import textwrap
import contextlib
from typing import Annotated

import markdown2
from atproto import AsyncClient, models
from fastapi import FastAPI, File, UploadFile, Request, Response
from fastapi.responses import HTMLResponse

from .zip_image import encode, decode

app = FastAPI()

hash_alg = os.environ.get("HASH_ALG", "sha256")
atproto_base_url = os.environ["ATPROTO_BASE_URL"]
atproto_handle = os.environ["ATPROTO_HANDLE"]
atproto_password= os.environ["ATPROTO_PASSWORD"]

did_plcs = {}
markdown_html_content_by_file = {}
client = AsyncClient(
    base_url=atproto_base_url,
)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    markdown_content = pathlib.Path(
        __file__
    ).parents[2].joinpath(
        "README.md",
    ).read_text()
    readme_markdown_html = markdown2.markdown(
        markdown_content,
        extras=[
            "fenced-code-blocks",
            "code-friendly",
            "highlightjs-lang",
        ],
    )
    markdown_html_content_by_file["README.md"] = textwrap.dedent(
        f"""
        <html>
            <title>{markdown_content.split("\n")[0].replace("# ", "")}</title>
            <body>
                {readme_markdown_html}
            </body>
        </html>
        """.strip()
    )

    profile = await client.login(
        atproto_handle,
        atproto_password,
    )
    did_plcs[atproto_handle] = profile.did
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/")
async def create(request: Request):
    file_data = await request.body()
    hash_instance = hashlib.new(hash_alg)
    hash_instance.update(file_data)
    data_as_image_hash = hash_instance.hexdigest()
    data_as_image_hash = f"{hash_alg}:{data_as_image_hash}"
    _mimetype, data_as_image = encode(file_data)
    post = await client.send_image(
        text=data_as_image_hash,
        image=data_as_image,
        image_alt=data_as_image_hash,
    )
    return {
        "id": post.uri.split("/")[-1],
        "url": f'https://bsky.app/profile/{atproto_handle}/post/{post.uri.split("/")[-1]}',
        "uri": post.uri,
        "cid": post.cid,
    }

@app.get("/{post_id}")
async def get(post_id: str):
    post = await client.get_post(post_id)
    blob = await client.com.atproto.sync.get_blob(
        models.com.atproto.sync.get_blob.Params(
            cid=post.value.embed.images[0].image.ref.link,
            did=did_plcs[atproto_handle],
        ),
    )
    mimetype, output_bytes = decode(blob)
    return Response(content=output_bytes, media_type=mimetype)

@app.get("/", response_class=HTMLResponse)
async def root():
    return markdown_html_content_by_file["README.md"]
