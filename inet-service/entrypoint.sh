#!/bin/sh
set -e

# Configure routing if ROUTER_IP is set
if [ -n "$ROUTER_IP" ]; then
    echo "Configuring default gateway to $ROUTER_IP"
    # We need to allow failure here in case we are not running with NET_ADMIN or if the route already exists/fails
    ip route del default || true
    ip route add default via "$ROUTER_IP" || echo "Failed to add default route (missing NET_ADMIN?)"
fi

# Execute the passed command
exec "$@"
