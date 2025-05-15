:class:`~motor.motor_asyncio.AsyncIOMotorClient` -- Connection to MongoDB
=========================================================================

.. warning:: Motor will be deprecated on May 14th, 2026, one year after the production release of the PyMongo Async driver. Critical bug fixes will be made until May 14th, 2027.
  We strongly recommend that Motor users migrate to the PyMongo Async driver while Motor is still supported.
  To learn more, see `the migration guide <https://www.mongodb.com/docs/languages/python/pymongo-driver/current/reference/migration/>`_.

.. autoclass:: motor.motor_asyncio.AsyncIOMotorClient
  :members:

  .. describe:: client[db_name] || client.db_name

     Get the `db_name` :class:`AsyncIOMotorDatabase` on :class:`AsyncIOMotorClient` `client`.

     Raises :class:`~pymongo.errors.InvalidName` if an invalid database name is used.
