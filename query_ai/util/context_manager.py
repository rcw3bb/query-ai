from query_ai.database import is_existing_context, DBMgr
from query_ai.model import model_manager
from query_ai.util.text_util import TextUtil

def create_sample_context(db_manager: DBMgr):
    """
    Creates sample context data and inserts it into the database if it does not already exist.

    Args:
        db_manager (DBMgr): An instance of the database manager to execute database operations.

    Author: Ron Webb
    Since: 1.0.0
    """

    sample_texts = [
        "The quick brown fox jumps over the lazy dog. The fox is known for its agility and speed, while the dog is often characterized by its relaxed nature.",
        "A journey of a thousand miles begins with a single step. This proverb emphasizes the importance of starting and perseverance in achieving long-term goals.",
        "To be or not to be, that is the question. This famous line from Shakespeare's Hamlet reflects on the philosophical nature of existence and the challenges of life.",
        """
Artificial intelligence (AI) has transitioned from a science fiction fantasy to a tangible reality, rapidly permeating various aspects of modern life.  From the mundane recommendations of streaming services to the complex algorithms driving autonomous vehicles, AI's influence is undeniable and its potential impact, both positive and negative, is profound. This essay will explore the multifaceted nature of AI, examining its current applications, potential benefits, ethical considerations, and the challenges that lie ahead in navigating this algorithmic age.

Currently, AI manifests itself in a multitude of forms, each with its own specific capabilities. Machine learning, a subset of AI, focuses on enabling computers to learn from data without explicit programming. This allows systems to identify patterns, make predictions, and improve their performance over time.  Deep learning, a further specialization, utilizes artificial neural networks with multiple layers to process complex data, achieving remarkable results in areas like image recognition and natural language processing.  These advancements have led to the development of sophisticated AI applications that are transforming industries and reshaping our daily routines.

One prominent area of AI application is in automation.  From manufacturing robots to sophisticated chatbots, AI-powered systems are streamlining processes, increasing efficiency, and reducing costs. In healthcare, AI is being used for disease diagnosis, personalized medicine, and drug discovery.  AI algorithms can analyze medical images, predict patient outcomes, and even assist surgeons during complex procedures.  The financial sector also benefits from AI, with its use in fraud detection, risk management, and algorithmic trading.  Moreover, AI is revolutionizing the way we communicate and access information.  Virtual assistants like Siri and Alexa have become commonplace, and AI-powered translation tools are breaking down language barriers.  Search engines utilize complex algorithms to provide us with relevant information, and social media platforms leverage AI to personalize content feeds.

Beyond increased efficiency and automation, AI has the potential to address some of the world's most pressing challenges.  In healthcare, AI can accelerate the development of new treatments and improve access to care, particularly in remote areas.  In environmental science, AI can be used to model climate change, optimize resource management, and develop sustainable solutions.  AI can also play a crucial role in education, personalizing learning experiences and providing students with tailored support.  Furthermore, AI has the potential to create new jobs and industries, driving economic growth and innovation.

However, the rapid advancement of AI also raises significant ethical concerns.  One of the most pressing issues is the potential for job displacement due to automation. As AI-powered systems become more sophisticated, they are capable of performing tasks previously done by humans, leading to concerns about widespread unemployment.  Another ethical challenge is the bias embedded within AI algorithms.  Since AI systems learn from data, they can inherit and amplify existing societal biases, leading to discriminatory outcomes.  For example, facial recognition algorithms have been shown to be less accurate for people of color, raising concerns about their use in law enforcement.

Furthermore, the increasing reliance on AI raises questions about privacy and data security.  AI systems often require vast amounts of data to function effectively, raising concerns about the collection and use of personal information.  The potential for misuse of this data, whether through hacking or unauthorized surveillance, is a significant concern.  The development of autonomous weapons systems also presents a profound ethical dilemma.  The idea of machines making life-or-death decisions without human intervention raises serious questions about accountability and the potential for unintended consequences.

Addressing these challenges requires a multi-faceted approach.  Governments, researchers, and industry leaders must work together to develop ethical guidelines and regulations for the development and deployment of AI.  It is crucial to ensure that AI systems are fair, transparent, and accountable.  Furthermore, it is important to invest in education and training programs to prepare the workforce for the changing demands of the AI-driven economy.  We need to equip individuals with the skills necessary to adapt to new roles and opportunities.

Another critical aspect is fostering public understanding and engagement with AI.  The public needs to be informed about the potential benefits and risks of AI to participate in informed discussions about its future.  This includes addressing misconceptions and fears about AI, while also acknowledging the legitimate concerns about its impact on society.  International cooperation is also essential, as the challenges posed by AI transcend national borders.  Global collaboration is necessary to develop common standards and ethical frameworks for the responsible development and use of AI.

In conclusion, artificial intelligence is a powerful and transformative technology with the potential to reshape our world in profound ways.  While the benefits of AI are significant, we must also address the ethical concerns and challenges that arise from its development and deployment.  By fostering collaboration, promoting transparency, and prioritizing ethical considerations, we can harness the power of AI for the betterment of society.  Navigating this algorithmic age requires careful planning, thoughtful regulation, and ongoing dialogue to ensure that AI serves humanity, rather than the other way around.  The future of AI is not predetermined; it is up to us to shape it in a way that maximizes its benefits and minimizes its risks.
        """,
        "Deep learning is a subfield of machine learning that uses artificial neural networks with multiple layers to analyze data. These networks are inspired by the way the human brain works, with interconnected nodes that process information and learn from it.",
    ]

    # Insert sample data and embeddings
    for text in sample_texts:

        paragraphs = TextUtil.split_by_paragraph(text)

        for paragraph in paragraphs:

            text_util = TextUtil()
            cleaned_text = text_util.clean_text(paragraph)

            embeddings = model_manager.get_embeddings(cleaned_text)

            for embedding_record in embeddings:
                chunk = embedding_record[3]

                if is_existing_context(db_manager, chunk):
                    continue

                chunk_id = embedding_record[0]
                start_word = embedding_record[1]
                end_word = embedding_record[2]
                embedding = embedding_record[4]

                db_manager.execute(stmt="""
                INSERT INTO qa_embeddings (chunk_id, start_word, end_word, context, embedding) 
                VALUES (%s, %s, %s, %s, %s)
                """, stmt_vars=(chunk_id, start_word, end_word, chunk, embedding))