Motor GridFS Classes
====================

.. warning:: Motor will be deprecated on May 14th, 2026, one year after the production release of the PyMongo Async driver. Critical bug fixes will be made until May 14th, 2027.
  We strongly recommend that Motor users migrate to the PyMongo Async driver while Motor is still supported.
  To learn more, see `the migration guide <https://www.mongodb.com/docs/languages/python/pymongo-driver/current/reference/migration/>`_.

.. currentmodule:: motor.motor_tornado

Store blobs of data in `GridFS <http://dochub.mongodb.org/core/gridfs>`_.

.. seealso:: :ref:`Differences between PyMongo's and Motor's GridFS APIs
  <gridfs-differences>`.

.. seealso:: :doc:`web`

.. autoclass:: MotorGridFSBucket
  :members:

.. autoclass:: MotorGridIn
  :members:

.. autoclass:: MotorGridOut
  :members:

.. autoclass:: MotorGridOutCursor
  :members:
