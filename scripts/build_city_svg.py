
name: Generate data-driven city SVG

on:
  workflow_dispatch:
  schedule:
    - cron: "17 */12 * * *"

permissions:
  contents: write

concurrency:
  group: generate-city-svg
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Build SVG from GitHub API
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
        run: python3 scripts/build_city_svg.py

      - name: Commit updated skyline
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add assets/city-dev-animation.svg
          if git diff --staged --quiet; then
            echo "No SVG changes."
            exit 0
          fi
          git commit -m "chore: regenerate data-driven profile city SVG"
          git push
