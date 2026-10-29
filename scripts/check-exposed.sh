#!/usr/bin/env bash
# Pre-Launch Security Toolkit - Check 23: Exposed Files Scanner
# Target usage: ./scripts/check-exposed.sh [https://example.com]

TARGET="${1:-http://localhost:5000}"
echo "================================================================"
echo " Check 23: Exposed Files & Information Leakage Audit"
echo " Target: $TARGET"
echo "================================================================"

PATHS=(
  "/.env"
  "/.env.local"
  "/.env.production"
  "/.env.development"
  "/.env.backup"
  "/.env.bak"
  "/.env.old"
  "/.git/config"
  "/.git/HEAD"
  "/.gitignore"
  "/.DS_Store"
  "/.vscode/settings.json"
  "/.idea/workspace.xml"
  "/backup.zip"
  "/backup.tar.gz"
  "/db.sql"
  "/dump.sql"
  "/database.sql"
  "/database.sqlite"
  "/data.db"
  "/config.json"
  "/config.yml"
  "/docker-compose.yml"
  "/.npmrc"
  "/phpinfo.php"
  "/server-status"
  "/swagger.json"
  "/openapi.json"
  "/graphql"
)

LEAKS=0
SECURED=0

for p in "${PATHS[@]}"; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET$p")
  if [ "$STATUS" -eq 404 ] || [ "$STATUS" -eq 403 ]; then
    printf "  [SAFE %s]   %s\n" "$STATUS" "$p"
    ((SECURED++))
  else
    printf "  [LEAK %s]   %s\n" "$STATUS" "$p"
    ((LEAKS++))
  fi
done

echo ""
echo "================================================================"
echo " Summary: $SECURED/${#PATHS[@]} paths blocked. Leaks: $LEAKS"
echo "================================================================"

if [ "$LEAKS" -gt 0 ]; then
  exit 1
fi

