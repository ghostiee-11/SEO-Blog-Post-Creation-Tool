# 🚀 AI-Powered SEO Blog Creation Tool

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-ff4b4b)
![AI](https://img.shields.io/badge/AI-Llama3-purple)
![CMS](https://img.shields.io/badge/CMS-WordPress-21759b)

An end-to-end automation tool that **scrapes** trending e-commerce products, **researches** SEO keywords using AI agents, **writes** optimized blog content, and **publishes** directly to WordPress. 

Designed to streamline affiliate marketing and content creation workflows.

---

## 📋 Table of Contents
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Task Fulfillment](#-internship-task-fulfillment)

---

## ✨ Features

*   **🕵️‍♂️ Multi-Source Scraping:** Fetches trending products from **eBay Global Deals** and **Amazon Best Sellers**. Supports both "Search" and "Trending" modes.
*   **🧠 AI SEO Agent:** Uses **Llama-3 (via Groq)** to simulate Google Keyword Planner, generating high-volume primary keywords and long-tail secondary keywords.
*   **✍️ AI Writer Agent:** Generates Human-like, Markdown-formatted reviews (150-250 words) based on deep-scraped product details.
*   **🔌 Auto-Publishing:** One-click publishing to any **WordPress** site via REST API with automatic formatting and affiliate link insertion.
*   **🖥️ Interactive UI:** Built with **Streamlit** for a seamless, card-based user experience.

---

## 🏗 Architecture

The application follows a modular "Agentic" pipeline:

```mermaid
graph LR
    A[User/UI] -->|Select Source| B(Scraper Module)
    B -->|Fetch HTML| C{Amazon/eBay}
    C -->|Raw Data| D[Data Normalizer]
    D -->|Product Title| E[SEO Agent Llama-3]
    E -->|Keywords| F[Writer Agent Llama-3]
    F -->|Blog Content| G[Publisher Module]
    G -->|REST API| H((WordPress Site))
