#!/home/creed347/anaconda3/envs/fastAPI/bin/python


import uvicorn


def main():
    return uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=1,
    )


if __name__ == "__main__":
    main()
