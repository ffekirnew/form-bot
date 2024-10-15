from formbot import App


async def main():
    app = App()

    await app.start()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
