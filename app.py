from flask import Flask, request, jsonify
import boto3, uuid, json

app = Flask(__name__)

comprehend = boto3.client("comprehend", region_name="us-east-1")
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
tabla = dynamodb.Table("g3-resenas")

@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.get_json() or {}
    texto = data.get("texto", "").strip()

    if not texto:
        return jsonify({"error": "Falta el campo 'texto'"}), 400

    s = comprehend.detect_sentiment(Text=texto, LanguageCode="es")
    f = comprehend.detect_key_phrases(Text=texto, LanguageCode="es")

    resultado = {
        "id": str(uuid.uuid4()),
        "texto": texto,
        "sentimiento": s["Sentiment"],
        "confianza": {k: str(round(v, 3)) for k, v in s["SentimentScore"].items()},
        "frases_clave": [p["Text"] for p in f["KeyPhrases"]],
    }

    tabla.put_item(Item=resultado)

    return jsonify(resultado), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
