integration:
    name: Integration Testing
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Resolve Missing Env File
        run: |
          mkdir -p api
          touch api/.env

      - name: Kill Existing Processes
        run: |
          sudo fuser -k 8000/tcp || true
          docker stop $(docker ps -aq) || true
          docker rm $(docker ps -aq) || true
          docker network prune -f

      - name: Start Services
        run: |
          docker compose up -d --build
          echo "Waiting for boot..."
          sleep 15

      - name: Check Startup Logs
        # This will show us WHY the API is failing before the test runs
        run: docker compose logs api

      - name: Run Integration Script
        run: |
          chmod +x scripts/integration-test.sh
          ./scripts/integration-test.sh

      - name: Cleanup
        if: always()
        run: docker compose down -v
