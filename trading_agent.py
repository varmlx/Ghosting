import os
import sys
import json
from typing import Dict, Any

import requests
from dotenv import load_dotenv


def get_base_url() -> str:
    base_url = os.getenv("RECALL_BASE_URL")
    if base_url:
        return base_url.rstrip("/")
    # Default to sandbox per docs
    return "https://api.sandbox.competitions.recall.network"


def read_api_key() -> str:
    api_key = os.getenv("RECALL_API_KEY")
    if not api_key:
        raise RuntimeError(
            "RECALL_API_KEY bulunamadı. Lütfen .env dosyasına ekleyin veya ortam değişkeni olarak ayarlayın."
        )
    return api_key


def execute_trade(payload: Dict[str, Any]) -> Dict[str, Any]:
    base_url = get_base_url()
    endpoint = f"{base_url}/api/trade/execute"
    api_key = read_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
    try:
        data = response.json()
    except Exception:
        data = {"text": response.text}

    if not response.ok:
        raise RuntimeError(f"Trade hatası: {response.status_code} {data}")

    return data


def main() -> None:
    load_dotenv()

    # Mainnet addresses (sandbox bir mainnet fork'u)
    from_token = os.getenv(
        "FROM_TOKEN",
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
    )
    to_token = os.getenv(
        "TO_TOKEN",
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
    )
    amount = os.getenv("AMOUNT_USDC", "100")
    reason = os.getenv("TRADE_REASON", "Quick-start verification trade")

    payload: Dict[str, Any] = {
        "fromToken": from_token,
        "toToken": to_token,
        "amount": amount,
        "reason": reason,
    }

    print("⏳  Recall'a trade isteği gönderiliyor …")
    try:
        result = execute_trade(payload)
    except Exception as exc:
        print("❌  Hata:", exc)
        sys.exit(1)

    print("✅  Trade başarılı:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


