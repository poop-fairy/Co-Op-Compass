Here’s the formatted README with proper spacing and code blocks:

---

# 🎮 Co-Op Compass: Finding Your Next Game Adventure!

Welcome to **Co-Op Compass**! This Python script helps you discover common games available on both PS5 and Xbox Game Pass. Say goodbye to FOMO and hello to gaming bliss!

## 🚀 Features

- Fetches game data from PS5 and Xbox Game Pass.
- Cleans and matches game titles using fuzzy logic (because who has perfect spelling?).
- Finds co-op games to make your gaming nights more fun!

## 📦 Requirements

Before you dive in, make sure you have:

- Python 3.6 or higher
- `fuzzywuzzy` library: 

  ```bash
  pip install fuzzywuzzy
  ```

- `requests` library: 

  ```bash
  pip install requests
  ```

## 🌐 API Keys

You'll need an API key for the RAWG API. Don't worry; it’s easy to get one! Just create an account on [RAWG](https://rawg.io/apidocs).

Once you have your API key, set it in your environment variables:

```bash
export MY_API_KEY="your_api_key_here"
```

## 🛠️ Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/Co-Op-Compass.git
```

Navigate to the project directory:

```bash
cd Co-Op-Compass
```

## 🎮 How to Use

Run the script to fetch and display common games:

```bash
python main.py
```

Sit back, relax, and let the game suggestions roll in!

## 🧩 Code Walkthrough

1. **Fetching Game Data**: It starts by pulling in PS5 and Xbox Game Pass data from their respective APIs.
2. **Cleaning Names**: Cleans up any unnecessary fluff in game titles (goodbye, PS4 & PS5 nonsense!).
3. **Finding Common Games**: Matches games from both platforms with fuzzy logic—because even game titles deserve a second chance.
4. **Searching RAWG API**: Looks up additional game data to enhance your experience.

## ⚠️ Troubleshooting

### Common Issues

- **Conflicts?** If you're merging branches and encounter conflicts, don’t panic! Resolve them using your favorite code editor and re-commit.
  
- **Missing API Key?** Ensure you've set your `MY_API_KEY` in your environment. You can do this in your terminal:

```bash
export MY_API_KEY="your_api_key_here"
```

## 🤝 Contributing

Want to help make Co-Op Compass even better? Fork this repository, make your changes, and submit a pull request. Let’s make gaming more accessible for everyone!

## 🎉 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to adjust any sections as needed!
