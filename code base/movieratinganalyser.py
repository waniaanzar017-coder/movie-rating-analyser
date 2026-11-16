import sys
import matplotlib.pyplot as plt
import pandas as pd


def analyze_movies(csv_filename):
  try:
    df = pd.read_csv(csv_filename)

    df.columns = df.columns.str.strip()

    required_cols = ["Movie", "Genre", "Rating"]
    for col in required_cols:
      if col not in df.columns:
        print(f"Error: Missing column '{col}'")
        return

    df = df.dropna(subset=required_cols)

    valid_rows = []
    for index, row in df.iterrows():
      try:
        rating_val = float(row["Rating"])
        if 0 <= rating_val <= 10:
          row["Rating"] = rating_val
          valid_rows.append(row)
        else:
          print(
              f"Row {index + 2} skipped: Rating {row['Rating']} must be between"
              " 0 and 10."
          )
      except ValueError:
        print(f"Row {index + 2} skipped: invalid Rating '{row['Rating']}'.")

    if not valid_rows:
      print("Error: No valid rows found!")
      return

    df = pd.DataFrame(valid_rows)
    df = df.drop_duplicates()

    print(f"Valid rows: {len(df)}")

    avg_rating = df["Rating"].mean()
    print(f"Average rating: {avg_rating:.2f}")

    max_rating = df["Rating"].max()
    top_movies = df[df["Rating"] == max_rating]["Movie"].tolist()
    print(f"Top-rated: {', '.join(top_movies)} ({max_rating})")

    min_rating = df["Rating"].min()
    lowest_movies = df[df["Rating"] == min_rating]["Movie"].tolist()
    print(f"Lowest: {', '.join(lowest_movies)} ({min_rating})")

    genre_grouped = df.groupby("Genre")["Rating"].mean()
    print("\nGenre-wise Average Ratings:")
    for genre, g_avg in genre_grouped.items():
      print(f"{genre}: {g_avg:.2f}")

    best_genre = genre_grouped.idxmax()
    print(f"Best genre: {best_genre}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    genre_grouped.plot(
        kind="bar", ax=axes[0], color="skyblue", edgecolor="black"
    )
    axes[0].set_title("Genre-wise Average Rating")
    axes[0].set_xlabel("Genre")
    axes[0].set_ylabel("Average Rating")
    axes[0].tick_params(axis="x", rotation=45)
    axes[0].grid(axis="y", linestyle="--", alpha=0.7)

    df["Rating"].plot(
        kind="hist",
        ax=axes[1],
        bins=5,
        color="salmon",
        edgecolor="black",
        range=(0, 10),
    )
    axes[1].set_title("Distribution of Movie Ratings")
    axes[1].set_xlabel("Rating")
    axes[1].set_ylabel("Frequency")
    axes[1].grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()

  except Exception as e:
    print(f"An error occurred: {e}")


if __name__ == "__main__":
  csv_file = sys.argv[1] if len(sys.argv) > 1 else "movies.csv"
  analyze_movies(csv_file)