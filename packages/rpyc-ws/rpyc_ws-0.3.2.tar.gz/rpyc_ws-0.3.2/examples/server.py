from rpyc_ws import create_rpyc_fastapi_app

app = create_rpyc_fastapi_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
