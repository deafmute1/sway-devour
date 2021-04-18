#!/usr/bin/env python
# -*- coding: utf-8 -*-

# stdlib
import os
import asyncio

# pypi
import click
from i3ipc.aio import Connection


@click.command()
@click.argument('executeable', nargs=1, required=True, type=str)
@click.option('--workspace',
              type=str,
              default='devour',
              nargs=1,
              help="Set name of workspace to devour to")
def main(executeable: str, workspace: str) -> None:
    """\b 
    sway-devour: a sway script to mimic the behavour of x11 window devourers  
        (such as bspwm's devour functionality or devour.c (SalmanAbedin@disroot.org)), 
        using a workspace instead of x11 (un)mapping to devour. 
    
    Version: 0.1

    Arguments:

        EXECUTEABLE    Some shell command to launch.  
    """
    d = Devour(executeable, workspace)
    asyncio.run(d.main())


class Devour:
    def __init__(self, executeable, workspace):
        self.workspace = workspace
        self.executeable = executeable
        self.spawned = None

    async def main(self):
        await self.connect()
        print("watch_window")
        await asyncio.gather(self.sway.main(), self.execute())

    async def connect(self):
        print("connect")
        self.sway = await Connection(auto_reconnect=True).connect()

        self.sway.on('window::new', self.handle_new_window)
        self.sway.on('window::close', self.handle_close_window)

        tree = await self.sway.get_tree()
        self.devoured = tree.find_focused()
        await self.sway.command("[con_id={}] move to workspace {}".format(
            self.devoured.id, self.workspace))

    async def execute(self):
        print("execute")
        os.system(self.executeable)

    async def handle_new_window(self, i3conn, event):
        print("handle new window")
        if self.spawned is None:
            self.spawned = event.container

    async def get_focused_workspace(self):
        workspaces = await self.sway.get_workspaces()
        for workspace in workspaces:
            if workspace.focused:
                return workspace
        return None

    async def handle_close_window(self, i3conn, event):
        print("handle close_window")
        if event.container.id == self.spawned.id:
            workspace = await self.get_focused_workspace()
            await self.sway.command("[con_id={}] move to workspace {}".format(
                self.devoured.id, workspace.name))
            self.sway.main_quit()

    async def get_focused_workspace(self):
        workspaces = await self.sway.get_workspaces()
        for workspace in workspaces:
            if workspace.focused:
                return workspace
        return None


if __name__ == '__main__':
    main()
