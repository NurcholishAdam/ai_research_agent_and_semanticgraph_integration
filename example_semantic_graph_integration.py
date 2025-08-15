#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: AI Research Agent with Semantic Graph Integration
Demonstrates the complete integration between research agent and semantic graph
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.research_agent import create_agent
from semantic_graph.ai_research_agent_integration import integrate_research_agent_with_semantic_graph
import uuid
import json

def demonstrate_integration():
    """Demonstrate the semantic graph integration with research agent"""
    
    print("🔗 AI Research Agent - Semantic Graph Integration Demo")
    print("=" * 60)
    
    # Step 1: Create research agent
    print("\n1️⃣ Creating AI Research Agent...")
    research_agent = create_agent()
    print("✅ Research agent created successfully")
    
    # Step 2: Integrate with semantic graph
    print("\n2️⃣ Integrating with Semantic Graph...")
    try:
        integration = integrate_research_agent_with_semantic_graph(research_agent)
        print("✅ Semantic graph integration completed")
        
        # Show integration statistics
        stats = integration.get_integration_statistics()
        print(f"   📊 Integration points active: {stats['hooks_registered']}")
        print(f"   🧠 Semantic graph nodes: {stats['semantic_graph_stats']['graph_core']['total_nodes']}")
        print(f"   🔗 Semantic graph edges: {stats['semantic_graph_stats']['graph_core']['total_edges']}")
        
    except Exception as e:
        print(f"❌ Integration failed: {e}")
        print("   Continuing with standard research agent...")
        integration = None
    
    # Step 3: Run research with integration
    print("\n3️⃣ Running Research with Semantic Graph Enhancement...")
    
    research_question = "What are the latest developments in large language models?"
    print(f"   🔬 Research Question: {research_question}")
    
    # Initialize enhanced state
    session_id = str(uuid.uuid4())
    initial_state = {
        "messages": [],
        "research_question": research_question,
        "research_plan": [],
        "current_step": 0,
        "findings": [],
        "final_answer": "",
        "iteration_count": 0,
        "hypotheses": [],
        "multi_agent_analysis": {},
        "quality_assessment": {},
        "intelligence_insights": {},
        "session_id": session_id,
        "rlhf_feedback": {},
        "reward_scores": {},
        "context_orchestration": {},
        "research_context": {},
        "diffusion_enhanced": False,
        "synthetic_contexts": [],
        "visual_analysis_results": {},
        "creative_ideas": {}
    }
    
    try:
        # Run research
        print("\n   🚀 Starting research execution...")
        result = research_agent.invoke(initial_state)
        
        print("\n✅ Research completed successfully!")
        
        # Display results
        print(f"\n📋 Research Plan ({len(result['research_plan'])} steps):")
        for i, step in enumerate(result["research_plan"], 1):
            print(f"   {i}. {step}")
        
        print(f"\n🔍 Research Steps Completed: {len(result['findings'])}")
        
        print(f"\n🎯 Final Answer Preview:")
        answer_preview = result["final_answer"][:300] + "..." if len(result["final_answer"]) > 300 else result["final_answer"]
        print(f"   {answer_preview}")
        
        # Show semantic graph integration benefits
        if integration:
            print("\n4️⃣ Semantic Graph Integration Benefits:")
            
            # Get updated statistics
            updated_stats = integration.get_integration_statistics()
            integration_events = updated_stats['integration_stats']
            
            print(f"   📝 Memory writes captured: {integration_events['memory_writes']}")
            print(f"   🛠️ Tool usage logged: {integration_events['tool_usage_logs']}")
            print(f"   🔍 Findings captured: {integration_events['findings_captured']}")
            print(f"   📊 Retrieval calls enhanced: {integration_events['retrieval_calls']}")
            print(f"   📋 Plan generations guided: {integration_events['plan_generations']}")
            print(f"   👤 Preference logs recorded: {integration_events['preference_logs']}")
            print(f"   📈 Monitoring events tracked: {integration_events['monitoring_events']}")
            
            # Show graph growth
            final_graph_stats = updated_stats['semantic_graph_stats']['graph_core']
            print(f"\n   🧠 Final graph size:")
            print(f"      Nodes: {final_graph_stats['total_nodes']}")
            print(f"      Edges: {final_graph_stats['total_edges']}")
            
            # Show node type distribution
            if final_graph_stats['node_types']:
                print(f"   📊 Node types created:")
                for node_type, count in final_graph_stats['node_types'].items():
                    print(f"      {node_type}: {count}")
            
            # Get integration health
            health = integration.get_integration_health()
            print(f"\n   💚 Integration Health: {health['status']}")
            print(f"   📈 Total events processed: {health['total_events_processed']}")
            
            # Process any pending graph events
            print("\n   🔄 Processing pending graph events...")
            integration.process_pending_events()
            print("   ✅ Graph events processed")
        
        return result, integration
        
    except Exception as e:
        print(f"❌ Research execution failed: {str(e)}")
        return None, integration

def demonstrate_graph_features(integration):
    """Demonstrate specific semantic graph features"""
    
    if not integration:
        print("⚠️ No integration available for graph feature demonstration")
        return
    
    print("\n5️⃣ Semantic Graph Features Demonstration:")
    print("-" * 50)
    
    # Demonstrate enhanced retrieval
    print("\n🔍 Enhanced Retrieval Example:")
    try:
        retrieval_result = integration.semantic_graph.enhanced_retrieval(
            query="machine learning models",
            strategy="hybrid",
            top_k=5
        )
        
        print(f"   Query: 'machine learning models'")
        print(f"   Strategy: hybrid (vector + graph)")
        print(f"   Results found: {len(retrieval_result.get('results', []))}")
        
        for i, result in enumerate(retrieval_result.get('results', [])[:3], 1):
            print(f"   {i}. {result['label']} (score: {result['score']:.3f})")
            print(f"      Method: {result['method']}")
            
    except Exception as e:
        print(f"   ❌ Enhanced retrieval demo failed: {e}")
    
    # Demonstrate graph-aware planning
    print("\n📋 Graph-Aware Planning Example:")
    try:
        planning_result = integration.semantic_graph.enhanced_planning(
            research_question="How do neural networks learn?",
            strategy="graph_guided",
            max_steps=5
        )
        
        print(f"   Question: 'How do neural networks learn?'")
        print(f"   Strategy: graph_guided")
        print(f"   Steps generated: {len(planning_result.get('plan_steps', []))}")
        
        for step in planning_result.get('plan_steps', [])[:3]:
            print(f"   • {step['description']}")
            if step.get('tools_suggested'):
                print(f"     Tools: {', '.join(step['tools_suggested'][:2])}")
                
    except Exception as e:
        print(f"   ❌ Graph-aware planning demo failed: {e}")
    
    # Demonstrate user preference modeling
    print("\n👤 User Preference Modeling Example:")
    try:
        # Record a sample preference
        preference_id = integration.semantic_graph.record_user_feedback(
            user_id="demo_user",
            preferred_content="Detailed technical explanations with examples",
            rejected_content="Brief superficial overviews",
            feedback_type="style",
            confidence=0.9
        )
        
        print(f"   Preference recorded: {preference_id}")
        
        # Get generation guidance
        guidance = integration.semantic_graph.get_generation_guidance("demo_user")
        
        if guidance.get('guidance_available'):
            print(f"   Guidance available: Yes")
            print(f"   Primary focus: {guidance.get('guidance', {}).get('primary_focus', 'N/A')}")
        else:
            print(f"   Guidance available: No (using defaults)")
            
    except Exception as e:
        print(f"   ❌ User preference demo failed: {e}")
    
    # Show comprehensive statistics
    print("\n📊 Comprehensive Graph Statistics:")
    try:
        stats = integration.semantic_graph.get_comprehensive_stats()
        
        print(f"   Graph Core:")
        print(f"     Total Nodes: {stats['graph_core']['total_nodes']}")
        print(f"     Total Edges: {stats['graph_core']['total_edges']}")
        
        print(f"   Ingestion Engine:")
        ingestion_stats = stats['ingestion']
        print(f"     Events Processed: {ingestion_stats['processing_stats']['events_processed']}")
        print(f"     Nodes Created: {ingestion_stats['processing_stats']['nodes_created']}")
        print(f"     Edges Created: {ingestion_stats['processing_stats']['edges_created']}")
        
        print(f"   Monitoring:")
        monitoring_stats = stats['monitoring']
        print(f"     Health Score: {monitoring_stats['health_score']:.3f}")
        print(f"     Health Status: {monitoring_stats['health_status']}")
        
    except Exception as e:
        print(f"   ❌ Statistics demo failed: {e}")

def main():
    """Main demonstration function"""
    
    try:
        # Run the main integration demonstration
        result, integration = demonstrate_integration()
        
        if result:
            # Demonstrate specific graph features
            demonstrate_graph_features(integration)
            
            print("\n🎉 Integration Demonstration Complete!")
            print("=" * 60)
            print("The semantic graph has enhanced the research agent with:")
            print("• Graph-aware retrieval for better context discovery")
            print("• Intelligent planning guided by knowledge relationships")
            print("• User preference modeling for personalized responses")
            print("• Comprehensive monitoring and health tracking")
            print("• Entity extraction and relationship discovery")
            print("• Citation tracking and knowledge graph construction")
            
            # Save results for inspection
            if integration:
                try:
                    final_stats = integration.get_integration_statistics()
                    with open('integration_demo_results.json', 'w') as f:
                        json.dump(final_stats, f, indent=2, default=str)
                    print(f"\n💾 Integration statistics saved to 'integration_demo_results.json'")
                except Exception as e:
                    print(f"⚠️ Could not save results: {e}")
        
        else:
            print("\n❌ Demonstration failed - check error messages above")
            
    except KeyboardInterrupt:
        print("\n\n👋 Demonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ Demonstration failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()