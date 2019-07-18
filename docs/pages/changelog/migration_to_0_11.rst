Migration guide to 0.11
=======================

In this version we have changed several violation codes.

Here's the full list:

.. code::

  436 -> 500
  437 -> 501
  451 -> 502
  457 -> 503
  463 -> 504
  464 -> 505
  467 -> 506
  468 -> 507
  470 -> 508
  472 -> 509
  473 -> 510
  474 -> 511
  475 -> 512

  ---

  465 -> 337

  ---

  426 -> 600
  427 -> 601
  433 -> 602
  434 -> 603
  452 -> 604
  453 -> 605
  454 -> 606
  455 -> 607
  456 -> 608
  462 -> 609

  ---

  459 -> 404
  460 -> 405
  461 -> 406
  466 -> 407
  469 -> 408
  471 -> 409

  446 -> 414
  447 -> 415
  448 -> 416
  449 -> 417
  450 -> 418
  458 -> 419

  442 -> 426
  443 -> 427
  444 -> 428
  445 -> 429

  435 -> 433
  438 -> 434
  439 -> 435
  440 -> 436
  441 -> 437

Make sure that you follow it in the correct order.
You can use ``sed`` to find all code and replace it to new ones.

That's what I did for our own source code.

