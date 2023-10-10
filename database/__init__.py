""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""


import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection
    async def get_blacklisted_users(self) -> list:
        """
        This function will return the list of all blacklisted users.

        :param user_id: The ID of the user that should be checked.
        :return: True if the user is blacklisted, False if not.
        """
        rows = await self.connection.execute("SELECT user_id, strftime('%s', created_at) FROM blacklist",
                
            )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            
            return result_list

    async def is_blacklisted(self,user_id: int) -> bool:
        """
        This function will check if a user is blacklisted.

        :param user_id: The ID of the user that should be checked.
        :return: True if the user is blacklisted, False if not.
        """
        async with self.connection.execute("SELECT * FROM blacklist WHERE user_id=?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result is not None


    async def add_user_to_blacklist(self,user_id: int) -> int:
        """
        This function will add a user based on its ID in the blacklist.

        :param user_id: The ID of the user that should be added into the blacklist.
        """
        await self.connection.execute("INSERT INTO blacklist(user_id) VALUES (?)", (user_id,))
        await self.connection.commit()
        rows = await self.connection.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0        

    async def remove_user_from_blacklist(self,user_id: int) -> int:
        """
        This function will add a user based on its ID in the blacklist.

        :param user_id: The ID of the user that should be added into the blacklist.
        """
        await self.connection.execute("DELETE FROM blacklist WHERE user_id=?", (user_id,))
        await self.connection.commit()
        rows = await self.connection.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0      

    async def add_warn(
        self, user_id: int, server_id: int, moderator_id: int, reason: str
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await self.connection.execute(
                "INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                (
                    warn_id,
                    user_id,
                    server_id,
                    moderator_id,
                    reason,
                ),
            )
            await self.connection.commit()
            return warn_id

    async def remove_warn(self, warn_id: int, user_id: int, server_id: int) -> int:
        """
        This function will remove a warn from the database.

        :param warn_id: The ID of the warn.
        :param user_id: The ID of the user that was warned.
        :param server_id: The ID of the server where the user has been warned
        """
        await self.connection.execute(
            "DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?",
            (
                warn_id,
                user_id,
                server_id,
            ),
        )
        await self.connection.commit()
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

    async def get_warnings(self, user_id: int, server_id: int) -> list:
        """
        This function will get all the warnings of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the warnings of the user.
        """
        rows = await self.connection.execute(
            "SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at), id FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list
