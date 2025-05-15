Prometheus Exporter for Technitium DNS
======================================

Yet another Prometheus exporter for the Technitium DNS server. There are
already two great ones by `NathanPERIER <https://github.com/NathanPERIER/technitium-dns-prometheus-exporter>`_
and `Work-m8 <https://github.com/Work-m8/technitium-prometheus-exporter>`_,
so why another? They each output a subset of the available metrics. I wanted them all.


Prerequisites
~~~~~~~~~~~~~

- You must have a Techitium DNS server running, obviously.
- Generate an API key in Technitium.


Creating the API token
~~~~~~~~~~~~~~~~~~~~~~

The exporter needs a read-only API token to talk to Technitium. Here's the recommended way to generate one:

1. Open your Technitium instance in a browser.
2. Navigate to **Administration > Groups** and create a group named "read-only".
3. Now create a user named "readonly" and make them a member of the group.
4. Go to **Administration > Permissions** and verify that Everyone has read-only access to everything.
5. Log out of Technitium. Log back in as the readonly user you just created.
6. Click on your profile in the top-right corner and select "Create API token".


Installation
~~~~~~~~~~~~

By far the easiest way to install this is with
`pipx <https://pipx.pypa.io/latest/>`__:

.. code:: bash

   pipx install technitium-exporter


Configuration
~~~~~~~~~~~~~

For your convenience, the exporter can be configured from environment
variables or command-line options, or a combination of both.

+--------------------+----------------------+---------------+-------------+--------------------------------------------------------------------+
| **Option**         | **Env Var**          | **Required?** | **Default** | **Meaning**                                                        |
+====================+======================+===============+=============+====================================================================+
| --address          | ``ADDRESS``          | No            | 0.0.0.0     | Interface to listen on for requests from Prometheus scrapers       |
+--------------------+----------------------+---------------+-------------+--------------------------------------------------------------------+
| --port             | ``PORT``             | No            | 9080        | Port number to listen on                                           |
+--------------------+----------------------+---------------+-------------+--------------------------------------------------------------------+
| --url              | ``TECHNITIUM_API``   | Yes           | None        | URL to the Technitium DNS API                                      |
+--------------------+----------------------+---------------+-------------+--------------------------------------------------------------------+
| --token            | ``TECHNITIUM_TOKEN`` | Yes           | None        | API token for Technitium                                           |
+--------------------+----------------------+---------------+-------------+--------------------------------------------------------------------+
| --all-record-types | None                 | No            | False       | Include counts for all DNS record types, not just the most popular |
+--------------------+----------------------+---------------+-------------+--------------------------------------------------------------------+


Metrics
~~~~~~~

Here's a sample of the output you can expect:

.. code:: text

   # HELP python_gc_objects_collected_total Objects collected during gc
   # TYPE python_gc_objects_collected_total counter
   python_gc_objects_collected_total{generation="0"} 420.0
   python_gc_objects_collected_total{generation="1"} 0.0
   python_gc_objects_collected_total{generation="2"} 0.0
   # HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
   # TYPE python_gc_objects_uncollectable_total counter
   python_gc_objects_uncollectable_total{generation="0"} 0.0
   python_gc_objects_uncollectable_total{generation="1"} 0.0
   python_gc_objects_uncollectable_total{generation="2"} 0.0
   # HELP python_gc_collections_total Number of times this generation was collected
   # TYPE python_gc_collections_total counter
   python_gc_collections_total{generation="0"} 58.0
   python_gc_collections_total{generation="1"} 5.0
   python_gc_collections_total{generation="2"} 0.0
   # HELP python_info Python platform information
   # TYPE python_info gauge
   python_info{implementation="CPython",major="3",minor="9",patchlevel="17",version="3.9.17"} 1.0
   # HELP technitium_update_available Returns 1 if there is a newer version of Technitium
   # TYPE technitium_update_available gauge
   technitium_update_available 0.0
   # HELP technitium_stats_queries_total Total number of DNS queries received by the server
   # TYPE technitium_stats_queries_total counter
   technitium_stats_queries_total 1763.0
   # HELP technitium_stats_no_error_total Total number of queries resolved without error
   # TYPE technitium_stats_no_error_total counter
   technitium_stats_no_error_total 1388.0
   # HELP technitium_stats_server_failure_total Total number of queries with SERVFAIL result
   # TYPE technitium_stats_server_failure_total counter
   technitium_stats_server_failure_total 0.0
   # HELP technitium_stats_nx_domain_total Total number of queries with NXDOMAIN result
   # TYPE technitium_stats_nx_domain_total counter
   technitium_stats_nx_domain_total 375.0
   # HELP technitium_stats_refused_total Total number of queries refused
   # TYPE technitium_stats_refused_total counter
   technitium_stats_refused_total 0.0
   # HELP technitium_stats_authoritative_total Total number of queries resolved as authoritative
   # TYPE technitium_stats_authoritative_total counter
   technitium_stats_authoritative_total 1546.0
   # HELP technitium_stats_recursive_total Total number of queries resolved recursively
   # TYPE technitium_stats_recursive_total counter
   technitium_stats_recursive_total 15.0
   # HELP technitium_stats_cached_total Total number of results cached
   # TYPE technitium_stats_cached_total counter
   technitium_stats_cached_total 196.0
   # HELP technitium_stats_blocked_total Total number of queries blocked
   # TYPE technitium_stats_blocked_total counter
   technitium_stats_blocked_total 6.0
   # HELP technitium_stats_dropped_total Total number of queries dropped
   # TYPE technitium_stats_dropped_total counter
   technitium_stats_dropped_total 0.0
   # HELP technitium_stats_clients_total Number of clients using the DNS
   # TYPE technitium_stats_clients_total counter
   technitium_stats_clients_total 35.0
   # HELP technitium_stats_zones Number of zones managed by the DNS
   # TYPE technitium_stats_zones gauge
   technitium_stats_zones 14.0
   # HELP technitium_stats_cached_entries Number of DNS entries cached by the server
   # TYPE technitium_stats_cached_entries gauge
   technitium_stats_cached_entries 10053.0
   # HELP technitium_stats_allowed_zones Number of zones explicitely allowed by the DNS
   # TYPE technitium_stats_allowed_zones gauge
   technitium_stats_allowed_zones 0.0
   # HELP technitium_stats_blocked_zones Number of zones blocked by the DNS
   # TYPE technitium_stats_blocked_zones gauge
   technitium_stats_blocked_zones 0.0
   # HELP technitium_stats_allow_list_zones Number of zones in the allow lists of the DNS
   # TYPE technitium_stats_allow_list_zones gauge
   technitium_stats_allow_list_zones 0.0
   # HELP technitium_stats_block_list_zones Number of zones in the block lists of the DNS
   # TYPE technitium_stats_block_list_zones gauge
   technitium_stats_block_list_zones 252411.0
   # HELP technitium_top_clients Top 10 clients by number of requests
   # TYPE technitium_top_clients gauge
   technitium_top_clients{domain="prometheus.svc",name="10.0.3.109",rank="1",rateLimited="False"} 538.0
   technitium_top_clients{domain="caddy.svc",name="192.168.2.151",rank="2",rateLimited="False"} 112.0
   technitium_top_clients{domain="plex.svc",name="192.168.14.150",rank="3",rateLimited="False"} 98.0
   technitium_top_clients{domain="uptime-kuma.svc",name="10.0.3.135",rank="4",rateLimited="False"} 94.0
   technitium_top_clients{domain="linkwarden.svc",name="10.0.3.125",rank="5",rateLimited="False"} 72.0
   technitium_top_clients{domain="homarr.svc",name="10.0.3.123",rank="6",rateLimited="False"} 72.0
   technitium_top_clients{domain="openobserve.svc",name="10.0.3.124",rank="7",rateLimited="False"} 72.0
   technitium_top_clients{domain="overseerr.svc",name="10.0.3.106",rank="8",rateLimited="False"} 52.0
   technitium_top_clients{domain="sonarr.svc",name="10.0.3.114",rank="9",rateLimited="False"} 52.0
   technitium_top_clients{domain="homebridge.svc",name="10.0.3.105",rank="10",rateLimited="False"} 49.0
   # HELP technitium_top_domains Top 10 domains requested for lookup
   # TYPE technitium_top_domains gauge
   technitium_top_domains{name="otel.svc",rank="1"} 786.0
   technitium_top_domains{name="sabnzbd",rank="2"} 56.0
   technitium_top_domains{name="plex.svc",rank="3"} 50.0
   technitium_top_domains{name="dartagnan.pve",rank="4"} 38.0
   technitium_top_domains{name="deluge",rank="5"} 26.0
   technitium_top_domains{name="www.google.com",rank="6"} 24.0
   technitium_top_domains{name="athos.pve",rank="7"} 22.0
   technitium_top_domains{name="porthos.pve",rank="8"} 22.0
   technitium_top_domains{name="otel",rank="9"} 17.0
   technitium_top_domains{name="uptime-kuma.svc",rank="10"} 16.0
   # HELP technitium_top_blocked Top 10 blocked domains
   # TYPE technitium_top_blocked gauge
   technitium_top_blocked{name="www.googletagmanager.com",rank="1"} 5.0
   technitium_top_blocked{name="logs.netflix.com",rank="2"} 1.0
   # HELP technitium_dns_request_result_count Number of requests with the given result
   # TYPE technitium_dns_request_result_count gauge
   technitium_dns_request_result_count{result="total"} 887.0
   technitium_dns_request_result_count{result="no_error"} 694.0
   technitium_dns_request_result_count{result="server_failure"} 0.0
   technitium_dns_request_result_count{result="nx_domain"} 193.0
   technitium_dns_request_result_count{result="refused"} 0.0
   # HELP technitium_dns_resolve_mode_count Number of requests resolved in a given mode
   # TYPE technitium_dns_resolve_mode_count gauge
   technitium_dns_resolve_mode_count{result="authoritative"} 775.0
   technitium_dns_resolve_mode_count{result="recursive"} 2.0
   technitium_dns_resolve_mode_count{result="cached"} 104.0
   technitium_dns_resolve_mode_count{result="blocked"} 6.0
   technitium_dns_resolve_mode_count{result="dropped"} 0.0
   # HELP technitium_record_type_count Number of responses by record type
   # TYPE technitium_record_type_count gauge
   technitium_record_type_count{desc="IPv4 address",record_type="A"} 738.0
   technitium_record_type_count{desc="IPv6 address",record_type="AAAA"} 523.0
   technitium_record_type_count{desc="Canonical name",record_type="CNAME"} 0.0
   technitium_record_type_count{desc="Mail exchange",record_type="MX"} 0.0
   technitium_record_type_count{desc="Name server",record_type="NS"} 0.0
   technitium_record_type_count{desc="Canonical name pointer",record_type="PTR"} 0.0
   technitium_record_type_count{desc="Start of authority",record_type="SOA"} 0.0
   technitium_record_type_count{desc="Service locator",record_type="SRV"} 484.0
   technitium_record_type_count{desc="Human-readable text",record_type="TXT"} 0.0
   # HELP technitium_protocol_type_count Number of requests by protocol
   # TYPE technitium_protocol_type_count gauge
   technitium_protocol_type_count{protocol="Tcp"} 0.0
   technitium_protocol_type_count{protocol="Udp"} 0.0
   technitium_protocol_type_count{protocol="Tls"} 0.0
   technitium_protocol_type_count{protocol="Https"} 0.0
   technitium_protocol_type_count{protocol="Quic"} 0.0


Starting automatically with systemd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Coming soon.


Releasing
~~~~~~~~~

.. code:: bash

    bump2version {patch|minor|major}
    prerelease
    release


Author
~~~~~~

This package was created and is maintained by `Todd
Radel <mailto:todd@radel.us>`__.
