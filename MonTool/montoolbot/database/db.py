import os

import logging
import asyncpg

logger = logging.getLogger("tg_bot")


async def db_conn():
    """
    Establish and return an asynchronous PostgreSQL connection using environment variables.
    """
    try:
        conn = await asyncpg.connect(
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database=os.getenv('POSTGRES_DB'),
            host=os.getenv('POSTGRES_HOST'))
        return conn
    except Exception as error:
        logger.error(f"Error during connection to DB - {error}")


async def user_list(tg_id):
    """
    Retrieve user information by Telegram ID.
    """
    try:
        conn = await db_conn()
        u_list = await conn.fetch('SELECT tg_id, tg_name, email, phone FROM app_monuser WHERE tg_id=$1', tg_id)
        await conn.close()
        return u_list
    except Exception as error:
        logger.error(f"Error with getting user list - {error}")


async def update_user(tg_id, name, email, phone):
    """
    Update user information based on email.
    """
    try:
        conn = await db_conn()
        await conn.execute(
            "UPDATE app_monuser SET tg_id=$1, tg_name=$2, phone=$3 WHERE email=$4",
            tg_id, name, phone, email)
        await conn.close()
    except Exception as error:
        logger.error(f"Error during user update - {error}")


async def email_check(email):
    """
    Check if a user exists by email.
    """
    try:
        conn = await db_conn()
        email_list = await conn.fetchrow('SELECT * FROM app_monuser WHERE email=$1', email)
        await conn.close()
        return email_list
    except Exception as error:
        logger.error(f"Error with getting email list - {error}")


async def server_list(tg_id):
    """
    Retrieve list of servers associated with a Telegram user.
    """
    try:
        conn = await db_conn()
        user = await conn.fetchrow('SELECT id FROM app_monuser WHERE tg_id=$1', tg_id)
        s_list = await conn.fetch('SELECT server_name, server_ip, os_name, status FROM app_server WHERE owner_id=$1',
                                  user["id"])
        await conn.close()
        return s_list
    except Exception as error:
        logger.error(f"Error with getting server list - {error}")
