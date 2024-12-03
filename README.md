# ATProto based pastebin

GitHub: https://github.com/publicdomainrelay/atprotobin

Paste

```bash
curl -X POST -F file=@README.md https://paste.chadig.com
```

Retrive using id from paste reponse JSON (`| jq -r .id`)

```bash
curl -sf https://paste.chadig.com/$id
```

Paste and retrive

```bash
curl -sf https://paste.chadig.com/$(curl -X POST -F file=@README.md https://paste.chadig.com | tee /dev/stderr | jq -r .id)
```

Paste and retrive (development)

```bash
curl -sf http://localhost:8000/$(curl -X POST -F file=@src/atprotobin/cli.py http://localhost:8000/ | tee /dev/stderr | jq -r .id)
```

Start server

```bash
python -m pip install -U pip setuptools wheel
python -m pip install -e .
ATPROTO_BASE_URL=https://atproto.chadig.com ATPROTO_HANDLE=publicdomainrelay.atproto.chadig.com ATPROTO_PASSWORD=$(python -m keyring get publicdomainrelay@protonmail.com password.publicdomainrelay.atproto.chadig.com) python -m atprotobin
```

- References
  - https://bsky.app/profile/johnandersen777.bsky.social/post/3lc47yvadu22i

[![asciicast](https://asciinema.org/a/693007.svg)](https://asciinema.org/a/693007)

- TODO
  - Receive webhook from VCS, get OIDC token, get secret using OIDC, trigger
    push and pull for federated repo.
