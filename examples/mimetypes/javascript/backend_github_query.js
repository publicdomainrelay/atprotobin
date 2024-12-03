let text = "";
const decoder = new TextDecoder();
for await (const chunk of Deno.stdin.readable) {
  text += decoder.decode(chunk);
}
const input = JSON.parse(text);

const resp = await fetch("https://api.github.com/users/" + input["user"], {
  headers: {
    accept: "application/json",
  },
});

console.log(JSON.stringify(await resp.json()));
