"""
test
Chatbot بسيط باستخدام Anthropic API
====================================
المشروع ده بيعلمك:
1. إزاي تبعت رسائل لـ Claude API
2. إزاي تحافظ على "ذاكرة" المحادثة (conversation history)
3. إزاي تستقبل الرد بشكل streaming (كلمة كلمة، زي ChatGPT)
"""

import os
import anthropic
#from dotenv import load_dotenv

# ============================================
# الخطوة 1: إعداد الـ Client
# ============================================
# بنقرأ الـ API key من ملف .env بدل ما نعتمد على
# environment variables (أسهل وأضمن، خصوصًا على Windows)

#load_dotenv()  # ده بيقرأ ملف .env ويحط اللي فيه في os.environ

#Key added here not sent via environment
client = anthropic.Anthropic(
    api_key=os.environ.get("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")
)

MODEL = "claude-sonnet-4-6"  # الموديل اللي هنستخدمه


def chat():
    """الدالة الرئيسية اللي بتشغل المحادثة"""

    # ============================================
    # الخطوة 2: تاريخ المحادثة
    # ============================================
    # الـ API مالوش "ذاكرة" بنفسه - إحنا اللي لازم نبعت
    # كل المحادثة السابقة في كل مرة عشان الموديل "يفتكر"

    conversation_history = []

    print("=" * 50)
    print("🤖 Chatbot بسيط - اكتب 'خروج' عشان تقفل")
    print("=" * 50)

    while True:
        # الخطوة 3: ناخد رسالة من المستخدم
        user_input = input("\n👤 أنت: ").strip()

        if user_input.lower() in ["خروج", "exit", "quit"]:
            print("👋 مع السلامة!")
            break

        if not user_input:
            continue

        # نضيف رسالة المستخدم للتاريخ
        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # ============================================
        # الخطوة 4: نبعت الطلب للـ API مع Streaming
        # ============================================
        print("\n🤖 Claude: ", end="", flush=True)

        assistant_response = ""

        try:
            # stream=True بيخلي الرد يظهر كلمة كلمة بدل ما ننتظر كله
            with client.messages.stream(
                model=MODEL,
                max_tokens=1024,
                system="انت مساعد ذكي وودود. رد باللهجة اللي بيتكلم بيها المستخدم.",
                messages=conversation_history,
            ) as stream:
                for text in stream.text_stream:
                    print(text, end="", flush=True)
                    assistant_response += text

            print()  # سطر جديد بعد ما يخلص الرد

            # نضيف رد الموديل لتاريخ المحادثة كمان
            # (عشان يفتكر إيه اللي قاله في المرة الجاية)
            conversation_history.append({
                "role": "assistant",
                "content": assistant_response
            })

        except anthropic.APIError as e:
            print(f"\n❌ حصل خطأ: {e}")


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠️  لازم تحط الـ API key الأول!")
        print("1. اعمل ملف اسمه .env في نفس مجلد المشروع")
        print("2. حط فيه السطر ده (بمفتاحك الحقيقي):")
        print("   ANTHROPIC_API_KEY=sk-ant-api03-...")
    else:
        chat()
