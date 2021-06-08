<h3 align="center"><img src="https://raw.githubusercontent.com/fikisipi/sponggy/main/sponggy_logo.png" height="50" valign="middle"> a Python tool for installing Caddy</h3>
<hr>
<h3 align="center">just run <code>pip install sponggy</code><h5 align="center">(not affiliated with the original Caddy project)</h5></h3>

<p align="center">
Once pip install is complete, just start the server with <code><b>sponggy run</b></code>
<br><br>
<img src="https://raw.githubusercontent.com/fikisipi/sponggy/main/sponggy_screencap.gif" width="448">
<br><br>
It will find a proper GitHub release from <code><b>caddyserver/caddy</b></code> and put it into your script path.<br>
You can use <code>sponggy <b>&lt;cmd&gt;</b></code> with any usual command (<code><b>help/start/stop/upgrade/...</b></code>) and Caddyfiles.
</p>

## Non-root pip installs and PATH

In most cases you don't need root privileges, so `pip install --user` is a better choice. Make sure that
your local user's bin is in `$PATH`. For example, on Linux:

```bash
$ python3 -m site --user-base
/home/some-user/.local
$ export PATH="~/.local/bin:$PATH"
$ # ^^ put in .bashrc if not already
$ pip install --user sponggy
```

## License

Siddy is licensed under the Apache 2.0 license. **It is not affiliated to the Caddy project** or its original
authors. During invocation, it downloads the original Apache `LICENSE` of each GitHub release from the
`caddy/caddyserver` repository.

[💰 Donate to Matt Holt, Caddy's original author](https://github.com/sponsors/mholt)