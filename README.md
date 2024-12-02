# ATProto based pastebin

Paste and retrive

```bash
curl -sf http://localhost:8000/$(curl -X POST --data-binary @src/atprotobin/cli.py -H "Content-Type: text/plain" http://localhost:8000/ | tee /dev/stderr | jq -r .id)
```

Start server

```bash
ATPROTO_BASE_URL=https://atproto.chadig.com ATPROTO_HANDLE=publicdomainrelay.atproto.chadig.com ATPROTO_PASSWORD=$(python -m keyring get publicdomainrelay@protonmail.com password.publicdomainrelay.atproto.chadig.com) python -m atprotobin
```

- References
  - https://bsky.app/profile/johnandersen777.bsky.social/post/3lc47yvadu22i

[![asciicast](https://asciinema.org/a/693001.svg)](https://asciinema.org/a/693001)
