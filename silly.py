#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

Silly example of using psycopg2's async.

This is a completely useless async example that is forced to run synchronous.

You'll need a database named test (or change it to a database you have).

.. code-block:: bash

    $ createdb test

'''

import select

import psycopg2

def wait(conn):
    while 1:
        state = conn.poll()
        if state == psycopg2.extensions.POLL_OK:
            break
        elif state == psycopg2.extensions.POLL_WRITE:
            select.select([], [conn.fileno()], [])
        elif state == psycopg2.extensions.POLL_READ:
            select.select([conn.fileno()], [], [])

conn = psycopg2.connect(database='test', async=1)
wait(conn)
curs = conn.cursor()
curs.execute("SELECT pg_sleep(5); SELECT 42;")
wait(curs.connection)
row = curs.fetchone()

print(row)
