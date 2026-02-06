#!/bin/bash

echo "========================================="
echo "FINDING YOUR LOCAL IP ADDRESS"
echo "========================================="
echo ""

# Try different methods to find local IP
IP=$(hostname -I | awk '{print $1}')

if [ -z "$IP" ]; then
    IP=$(ip route get 8.8.8.8 2>/dev/null | awk 'NR==1 {print $7}')
fi

if [ -z "$IP" ]; then
    IP=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | head -1 | awk '{print $2}' | sed 's/addr://')
fi

if [ -n "$IP" ]; then
    echo "Your local IP address: $IP"
    echo ""
    echo "Access URLs:"
    echo "- Frontend: http://$IP:5173"
    echo "- Backend API: http://$IP:8000"
    echo "- API Docs: http://$IP:8000/docs"
    echo ""
    echo "Other devices on your LAN can access using these URLs"
else
    echo "Could not determine local IP address automatically."
    echo "Try one of these commands manually:"
    echo "  ifconfig | grep -E 'inet (192\.|10\.|172\.)'"
    echo "  ip addr show | grep -E 'inet (192\.|10\.|172\.)'"
fi