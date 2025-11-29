#!/bin/sh

echo "Running Prisma Generate..."
npx prisma generate

echo "Starting Backend (DEV mode)..."
npm run dev