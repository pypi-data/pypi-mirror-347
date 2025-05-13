if __name__ == "__main__":
    import asyncio

    from api import BaseTunaAPI

    async def main():
        # creating API-object and launching a tunnel
        api = BaseTunaAPI(input('API-key: '))
        running_tunnel = await api.run_tunnel('http', 8080)
        print(running_tunnel)

        # checking running tunnels and current processes
        tunnels = await api.get_tunnels(1, 1)
        print(tunnels)
        print(api.processes)

        # stopping a running tunnel and re-checking
        await api.stop_tunnel(tunnels[0].uid)
        tunnels = await api.get_tunnels(1, 1)
        print(tunnels)
        print(api.processes)

        # launching a new tunnels and test both modes of stop_tuna
        running_tunnel = await api.run_tunnel('http', 8080)
        print(running_tunnel)
        await api.stop_tuna(kill_session_only=False)

        running_tunnel = await api.run_tunnel('http', 8080)
        print(running_tunnel)
        await api.stop_tuna()

    asyncio.run(main())
