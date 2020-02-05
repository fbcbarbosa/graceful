# Graceful

Collection of containerized applications with proper signal handling, to show how to perform graceful shutdown within Docker and Kubernetes.

## uwsgi

So, UWSGI is a complex beast, and hardly the best option when it comes to containerized applications (or so I'm convinced). But I think I've managed to get hold of something that works.

Fiest, these two options are essential:

```ini
# when die-on-term is set, application will stop when SIGTERM is received
die-on-term = true

# master mode, recommended in production
master = true
```

Note that UWSG [does not support graceful stops/shutdowns](https://uwsgi-docs.readthedocs.io/en/latest/Management.html#signals-for-controlling-uwsgi) (only reloads). But you can use the `uwsgi.atext` library to trap the shutdown signal in the worker, and then do whatever you need to do.

There's some discussion that this can be flaky, so I'm testing it still, but it seems to work.

```python
# handle termination when running inside uwsgi
try:
    import uwsgi
    uwsgi.atexit = teardown
except Exception as exc:
    app.logger.info("uwsgi atexit handler not registered %s", exc)
    pass
```

When running your webserver without UWSGI, you can use the Python `signal` library to trap termination signals and then call a handler function:

```python
if __name__ == "__main__":

    # handle OS termination signals when running in standalone mode
    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, teardown)

    app.run(host="0.0.0.0", port=8000, threaded=True)
```