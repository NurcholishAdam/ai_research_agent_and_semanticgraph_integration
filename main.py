# -*- coding: utf-8 -*-
"""
AI Research Agent - Main Entry Point
Enhanced with proper state management and interactive capabilities
"""

from agent.research_agent import create_agent
from semantic_graph.ai_research_agent_integration import integrate_research_agent_with_semantic_graph
import json

def run_research(question: str, use_semantic_graph: bool = False):
    """Run a research session with the given question"""
    print(f"🔬 Starting research on: {question}")
    if use_semantic_graph:
        print("🕸️ Using Semantic Graph Enhancement")
    print("=" * 60)
    
    # Create the agent
    agent = create_agent()
    
    # Integrate with semantic graph if requested
    integration = None
    if use_semantic_graph:
        try:
            print("🔗 Integrating with Semantic Graph...")
            integration = integrate_research_agent_with_semantic_graph(agent)
            print("✅ Semantic Graph integration completed")
        except Exception as e:
            print(f"⚠️ Semantic Graph integration failed: {e}")
            print("   Continuing with standard research agent...")
    
    # Initialize state - Phase 6 Enhanced with RLHF
    import uuid
    session_id = str(uuid.uuid4())
    
    initial_state = {
        "messages": [],
        "research_question": question,
        "research_plan": [],
        "current_step": 0,
        "findings": [],
        "final_answer": "",
        "iteration_count": 0,
        # Phase 4 Intelligence Layer components
        "hypotheses": [],
        "multi_agent_analysis": {},
        "quality_assessment": {},
        "intelligence_insights": {},
        # Phase 6 RLHF components
        "session_id": session_id,
        "rlhf_feedback": {},
        "reward_scores": {}
    }
    
    try:
        # Run the research
        result = agent.invoke(initial_state)
        
        # Display results
        print("\n📋 Research Plan:")
        for i, step in enumerate(result["research_plan"], 1):
            print(f"  {i}. {step}")
        
        print(f"\n🔍 Research Steps Completed: {len(result['findings'])}")
        
        print("\n📊 Key Findings:")
        for finding in result["findings"]:
            print(f"\n  Step {finding['step'] + 1}: {finding['step_description']}")
            print(f"  Analysis: {finding['analysis'][:200]}...")
        
        print("\n🎯 Final Answer:")
        print("-" * 40)
        print(result["final_answer"])
        print("-" * 40)
        
        # Show semantic graph integration benefits if used
        if integration:
            print("\n🕸️ Semantic Graph Integration Benefits:")
            stats = integration.get_integration_statistics()
            integration_events = stats['integration_stats']
            
            print(f"   📝 Memory writes captured: {integration_events['memory_writes']}")
            print(f"   🛠️ Tool usage logged: {integration_events['tool_usage_logs']}")
            print(f"   🔍 Findings captured: {integration_events['findings_captured']}")
            print(f"   📊 Enhanced retrievals: {integration_events['retrieval_calls']}")
            print(f"   📋 Graph-guided plans: {integration_events['plan_generations']}")
            
            # Process pending graph events
            integration.process_pending_events()
        
        return result
        
    except Exception as e:
        print(f"❌ Error during research: {str(e)}")
        return None

def interactive_mode():
    """Run the agent in interactive mode"""
    print("🤖 AI Research Agent - Interactive Mode")
    print("Type 'quit' to exit, 'help' for commands")
    print("Type 'graph' to enable semantic graph enhancement")
    print("=" * 50)
    
    use_semantic_graph = False
    
    while True:
        try:
            question = input("\n🔬 Enter your research question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif question.lower() == 'help':
                print("\nAvailable commands:")
                print("  - Enter any research question to start research")
                print("  - 'graph' to toggle semantic graph enhancement")
                print("  - 'quit' or 'exit' to leave")
                print("  - 'help' to see this message")
                continue
            elif question.lower() == 'graph':
                use_semantic_graph = not use_semantic_graph
                status = "enabled" if use_semantic_graph else "disabled"
                print(f"🕸️ Semantic Graph enhancement {status}")
                continue
            elif not question:
                print("Please enter a valid research question.")
                continue
            
            # Run research
            result = run_research(question, use_semantic_graph)
            
            if result:
                # Ask if user wants to continue
                continue_research = input("\n🔄 Continue with another question? (y/n): ").strip().lower()
                if continue_research not in ['y', 'yes']:
                    print("👋 Research session ended!")
                    break
            
        except KeyboardInterrupt:
            print("\n\n👋 Research interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    # You can run in different modes
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode with question as argument
        use_graph = '--graph' in sys.argv
        if use_graph:
            sys.argv.remove('--graph')
        
        question = " ".join(sys.argv[1:])
        run_research(question, use_graph)
    else:
        # Interactive mode
        interactive_mode()