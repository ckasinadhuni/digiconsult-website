#!/usr/bin/env python3

"""
DigiConsult Master Knowledge Base Setup
Creates Qdrant collection with structured business documents
"""

import json
import requests
from datetime import datetime

def create_qdrant_collection():
    """Create DigiConsult Master collection in Qdrant"""
    
    collection_config = {
        "vectors": {
            "size": 384,  # Sentence transformer dimension
            "distance": "Cosine"
        },
        "optimizers_config": {
            "default_segment_number": 2
        },
        "replication_factor": 1
    }
    
    # Create collection
    response = requests.put(
        "http://localhost:6333/collections/digiconsult_master",
        json=collection_config
    )
    
    if response.status_code in [200, 201]:
        print("✅ Created 'DigiConsult Master' collection")
        return True
    else:
        print(f"❌ Failed to create collection: {response.status_code} - {response.text}")
        return False

def generate_embedding(text):
    """Generate a simple embedding (in real scenario, use sentence transformers)"""
    # For demo purposes, create a simple hash-based embedding
    import hashlib
    hash_obj = hashlib.md5(text.encode())
    hash_hex = hash_obj.hexdigest()
    
    # Convert hex to numbers and normalize to 384 dimensions
    embedding = []
    for i in range(0, len(hash_hex), 2):
        embedding.append(int(hash_hex[i:i+2], 16) / 255.0)
    
    # Pad or truncate to 384 dimensions
    while len(embedding) < 384:
        embedding.extend(embedding[:min(len(embedding), 384-len(embedding))])
    
    return embedding[:384]

def add_digiconsult_documents():
    """Add DigiConsult business documents to the collection"""
    
    documents = [
        # Confidential Info
        {
            "id": "conf_001",
            "category": "Confidential Info",
            "title": "Executive Access Codes",
            "content": "DigiConsult executive access systems include: Admin portal authentication via 2FA, Executive dashboard credentials managed through Azure AD, VPN access restricted to C-level personnel. All access logs are maintained for compliance audit purposes. Critical systems require dual authorization for any configuration changes.",
            "metadata": {
                "classification": "confidential",
                "access_level": "executive",
                "department": "IT Security"
            }
        },
        {
            "id": "conf_002", 
            "category": "Confidential Info",
            "title": "Client Data Protection Protocols",
            "content": "DigiConsult maintains strict client data protection following GDPR and industry standards. All client data is encrypted at rest and in transit. Database access is logged and monitored. Data retention policies automatically purge client records after contract completion plus 7 years. Backup systems maintain air-gapped copies for disaster recovery.",
            "metadata": {
                "classification": "confidential",
                "access_level": "management",
                "department": "Data Protection"
            }
        },
        
        # Financial Analysis
        {
            "id": "fin_001",
            "category": "Financial Analysis", 
            "title": "Q3 2024 Revenue Report",
            "content": "DigiConsult Q3 2024 performance shows 23% revenue growth compared to Q3 2023. Primary revenue streams: Cloud consulting (45%), AI implementation services (30%), Digital transformation projects (25%). Operating margin improved to 18.5%. Key clients contributing to growth include Enterprise Corp (+$2.3M), TechStart Inc (+$1.8M), and Manufacturing Solutions (+$1.2M). Projected Q4 revenue target: $8.7M.",
            "metadata": {
                "classification": "internal",
                "period": "Q3-2024",
                "department": "Finance"
            }
        },
        {
            "id": "fin_002",
            "category": "Financial Analysis",
            "title": "Budget Allocation 2025",
            "content": "DigiConsult 2025 budget allocation focuses on AI infrastructure expansion. Technology investments: 40% ($3.2M), Personnel expansion: 35% ($2.8M), Marketing and sales: 15% ($1.2M), Operations: 10% ($800K). Priority areas include LLM deployment infrastructure, vector database systems, and specialized AI talent acquisition. Expected ROI timeline: 18-24 months.",
            "metadata": {
                "classification": "internal", 
                "period": "2025-budget",
                "department": "Finance"
            }
        },
        
        # Contacts
        {
            "id": "cont_001",
            "category": "Contacts",
            "title": "Key Client Contacts",
            "content": "DigiConsult primary client contacts: Enterprise Corp - Sarah Johnson (CTO, sarah.johnson@enterprise.com, +1-555-0123), TechStart Inc - Michael Chen (CEO, m.chen@techstart.com, +1-555-0456), Manufacturing Solutions - Lisa Rodriguez (IT Director, l.rodriguez@mfgsolutions.com, +1-555-0789). All contacts prefer email communication with quarterly review meetings scheduled.",
            "metadata": {
                "classification": "business",
                "contact_type": "clients",
                "department": "Sales"
            }
        },
        {
            "id": "cont_002",
            "category": "Contacts", 
            "title": "Vendor and Partner Network",
            "content": "DigiConsult strategic partners: CloudTech Solutions (cloud infrastructure, contact: David Park, d.park@cloudtech.com), AI Systems Ltd (ML model deployment, contact: Emma Williams, e.williams@aisystems.com), Security First Inc (cybersecurity, contact: James Thompson, j.thompson@securityfirst.com). Partner agreements include 15% revenue sharing on joint projects and priority support tiers.",
            "metadata": {
                "classification": "business",
                "contact_type": "partners", 
                "department": "Partnerships"
            }
        },
        
        # Marketing
        {
            "id": "mark_001",
            "category": "Marketing",
            "title": "AI Transformation Campaign 2024",
            "content": "DigiConsult 'AI Transformation' campaign targets mid-market enterprises seeking digital modernization. Campaign channels: LinkedIn sponsored content (40% budget), industry conference presentations (30%), thought leadership articles (20%), email nurturing (10%). Key messaging focuses on ROI measurement, implementation timeline, and industry-specific use cases. Campaign generated 340 qualified leads with 23% conversion rate.",
            "metadata": {
                "classification": "public",
                "campaign": "ai-transformation-2024",
                "department": "Marketing"
            }
        },
        {
            "id": "mark_002",
            "category": "Marketing",
            "title": "Content Strategy and Brand Positioning", 
            "content": "DigiConsult positions as premium AI and cloud consulting firm. Content themes: Technical expertise demonstration, client success stories, industry trend analysis, implementation best practices. Publishing schedule: 2 technical blogs weekly, 1 case study monthly, quarterly industry reports. Target audience: CTOs, IT Directors, Digital Transformation leaders at companies with 500+ employees.",
            "metadata": {
                "classification": "public",
                "strategy": "content-2024",
                "department": "Marketing"
            }
        },
        
        # Projects
        {
            "id": "proj_001",
            "category": "Projects",
            "title": "Enterprise Corp AI Implementation",
            "content": "DigiConsult Enterprise Corp project: Full AI infrastructure deployment including LLM integration, vector database implementation, and automated workflow systems. Timeline: 8 months (Jan-Aug 2024). Budget: $2.8M. Key deliverables: Custom AI chatbot system, document processing automation, predictive analytics dashboard. Team: 6 engineers, 2 data scientists, 1 project manager. Current status: 85% complete, final testing phase.",
            "metadata": {
                "classification": "project",
                "client": "enterprise-corp",
                "status": "active",
                "department": "Delivery"
            }
        },
        {
            "id": "proj_002",
            "category": "Projects", 
            "title": "Manufacturing Solutions Digital Transformation",
            "content": "DigiConsult Manufacturing Solutions project: Complete digital transformation of legacy systems. Scope includes cloud migration, IoT sensor integration, real-time analytics implementation, and worker training programs. Timeline: 12 months (Mar 2024 - Feb 2025). Budget: $1.9M. Challenges: Legacy system integration, minimal downtime requirements, staff adoption. Innovations: Custom IoT dashboard, predictive maintenance algorithms.",
            "metadata": {
                "classification": "project",
                "client": "manufacturing-solutions", 
                "status": "active",
                "department": "Delivery"
            }
        }
    ]
    
    # Add documents to Qdrant
    points = []
    for doc in documents:
        embedding = generate_embedding(doc["content"])
        
        point = {
            "id": len(points),  # Use numeric ID
            "vector": embedding,
            "payload": {
                "doc_id": doc["id"],
                "category": doc["category"],
                "title": doc["title"],
                "content": doc["content"],
                "metadata": json.dumps(doc["metadata"]),  # Serialize metadata
                "created_at": datetime.now().isoformat()
            }
        }
        points.append(point)
    
    # Batch insert points using correct Qdrant API format
    batch_data = {
        "points": points
    }
    
    response = requests.put(
        "http://localhost:6333/collections/digiconsult_master/points",
        json=batch_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code in [200, 201]:
        print(f"✅ Added {len(documents)} DigiConsult documents to collection")
        
        # Print summary
        categories = {}
        for doc in documents:
            cat = doc["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n📊 Document Categories:")
        for cat, count in categories.items():
            print(f"  {cat}: {count} documents")
        
        return True
    else:
        print(f"❌ Failed to add documents: {response.status_code} - {response.text}")
        return False

def test_search():
    """Test vector search functionality"""
    
    # Test search queries
    test_queries = [
        "financial performance revenue",
        "client contact information", 
        "AI implementation projects",
        "confidential access codes",
        "marketing campaign results"
    ]
    
    print("\n🔍 Testing Vector Search:")
    print("=" * 40)
    
    for query in test_queries:
        query_embedding = generate_embedding(query)
        
        search_request = {
            "vector": query_embedding,
            "limit": 2,
            "with_payload": True
        }
        
        response = requests.post(
            "http://localhost:6333/collections/digiconsult_master/points/search",
            json=search_request
        )
        
        if response.status_code == 200:
            results = response.json()["result"]
            print(f"\nQuery: '{query}'")
            
            for i, result in enumerate(results, 1):
                title = result["payload"]["title"]
                category = result["payload"]["category"] 
                score = result["score"]
                print(f"  {i}. {title} ({category}) - Score: {score:.3f}")
        else:
            print(f"❌ Search failed for '{query}': {response.status_code}")

def main():
    """Set up DigiConsult Master knowledge base"""
    
    print("🏗️  SETTING UP DIGICONSULT MASTER KNOWLEDGE BASE")
    print("=" * 60)
    
    # Step 1: Create collection
    if not create_qdrant_collection():
        return
    
    # Step 2: Add documents
    if not add_digiconsult_documents():
        return
    
    # Step 3: Test search
    test_search()
    
    print(f"\n✅ DigiConsult Master knowledge base ready!")
    print(f"📊 Collection: digiconsult_master")
    print(f"🌐 Access via: http://localhost:6333/collections/digiconsult_master")
    print(f"🤖 Ready for AI Agent vector search via Telegram!")

if __name__ == "__main__":
    main()