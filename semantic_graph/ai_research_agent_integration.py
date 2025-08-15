# -*- coding: utf-8 -*-
"""
AI Research Agent - Semantic Graph Integration Points
Implements the integration mapping between research agent components and semantic graph
"""

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from .research_agent_integration import SemanticGraphAgent
from .graph_ingestion import IngestionSource
from .graph_core import NodeType, EdgeType

logger = logging.getLogger(__name__)

class AIResearchAgentIntegration:
    """Main integration class connecting AI Research Agent with Semantic Graph"""
    
    def __init__(self, semantic_graph_agent: SemanticGraphAgent):
        self.semantic_graph = semantic_graph_agent
        self.integration_hooks = {}
        self.integration_stats = {
            'memory_writes': 0,
            'tool_usage_logs': 0,
            'findings_captured': 0,
            'retrieval_calls': 0,
            'plan_generations': 0,
            'preference_logs': 0,
            'monitoring_events': 0
        }
        
        # Register integration hooks
        self._register_integration_hooks()
        
        logger.info("AI Research Agent - Semantic Graph integration initialized")
    
    def _register_integration_hooks(self):
        """Register all integration hooks based on the mapping table"""
        
        # Memory writes integration
        self.integration_hooks['memory_writes'] = self._handle_memory_output
        
        # Tool usage logs integration
        self.integration_hooks['tool_usage_logs'] = self._handle_tool_usage
        
        # Findings capture integration
        self.integration_hooks['findings_capture'] = self._handle_finding
        
        # Retrieval calls integration
        self.integration_hooks['retrieval_calls'] = self._handle_retrieval
        
        # Plan generation integration
        self.integration_hooks['plan_generation'] = self._handle_planning
        
        # Preference logging integration
        self.integration_hooks['preference_logging'] = self._handle_preference
        
        # Monitoring integration
        self.integration_hooks['monitoring'] = self._handle_monitoring
    
    # Integration Point 1: Memory writes -> GraphIngestionEngine.handle_memory_output()
    def _handle_memory_output(self, memory_data: Dict[str, Any]) -> str:
        """
        Hook: MemoryManager.write()
        What Happens: New nodes/edges created from extracted entities
        """
        try:
            # Extract memory content and metadata
            content = memory_data.get('content', '')
            importance = memory_data.get('importance', 0.5)
            memory_type = memory_data.get('memory_type', 'general')
            session_id = memory_data.get('session_id', 'default')
            
            # Prepare ingestion data
            ingestion_data = {
                'content': content,
                'importance': importance,
                'memory_type': memory_type,
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'source': 'memory_manager'
            }
            
            # Add concepts and citations if available
            if 'concepts' in memory_data:
                ingestion_data['concepts'] = memory_data['concepts']
            if 'citations' in memory_data:
                ingestion_data['citations'] = memory_data['citations']
            
            # Ingest into semantic graph
            self.semantic_graph.ingestion_engine.ingest_event(
                IngestionSource.MEMORY,
                ingestion_data,
                priority=2
            )
            
            self.integration_stats['memory_writes'] += 1
            
            return f"Memory content ingested into semantic graph: {len(content)} chars"
            
        except Exception as e:
            logger.error(f"Memory output integration failed: {e}")
            return f"Memory integration error: {str(e)}"
    
    # Integration Point 2: Tool usage logs -> GraphIngestionEngine.handle_tool_usage()
    def _handle_tool_usage(self, tool_data: Dict[str, Any]) -> str:
        """
        Hook: ToolExecutor.execute_tool()
        What Happens: Records "UsesTool" edges and merges duplicates
        """
        try:
            tool_name = tool_data.get('tool_name', '')
            tool_input = tool_data.get('tool_input', '')
            tool_output = tool_data.get('tool_output', '')
            execution_time = tool_data.get('execution_time', 0.0)
            success = tool_data.get('success', True)
            
            # Prepare tool usage data
            usage_data = {
                'tool_name': tool_name,
                'input': tool_input,
                'output': tool_output,
                'execution_time': execution_time,
                'success': success,
                'timestamp': datetime.now().isoformat(),
                'usage_context': tool_data.get('context', 'research')
            }
            
            # Ingest tool usage
            self.semantic_graph.ingestion_engine.ingest_event(
                IngestionSource.TOOL_USAGE,
                usage_data,
                priority=1
            )
            
            self.integration_stats['tool_usage_logs'] += 1
            
            return f"Tool usage logged: {tool_name} -> semantic graph"
            
        except Exception as e:
            logger.error(f"Tool usage integration failed: {e}")
            return f"Tool usage integration error: {str(e)}"
    
    # Integration Point 3: Findings capture -> GraphIngestionEngine.handle_finding()
    def _handle_finding(self, finding_data: Dict[str, Any]) -> str:
        """
        Hook: ResearchLoop.capture_finding()
        What Happens: Ingests summaries/triples into graph
        """
        try:
            finding_content = finding_data.get('finding', '')
            step_info = finding_data.get('step_info', {})
            confidence = finding_data.get('confidence', 0.5)
            sources = finding_data.get('sources', [])
            analysis = finding_data.get('analysis', '')
            
            # Prepare research finding data
            research_data = {
                'finding': finding_content,
                'analysis': analysis,
                'confidence': confidence,
                'sources': sources,
                'step_info': step_info,
                'research_step': step_info.get('step_number', 0),
                'timestamp': datetime.now().isoformat()
            }
            
            # Ingest research finding
            self.semantic_graph.ingestion_engine.ingest_event(
                IngestionSource.RESEARCH_FINDINGS,
                research_data,
                priority=2
            )
            
            self.integration_stats['findings_captured'] += 1
            
            return f"Research finding captured: {len(finding_content)} chars"
            
        except Exception as e:
            logger.error(f"Finding capture integration failed: {e}")
            return f"Finding capture error: {str(e)}"
    
    # Integration Point 4: Retrieval calls -> GraphAwareRetrieval.retrieve()
    def _handle_retrieval(self, retrieval_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook: Retriever.get_relevant()
        What Happens: Reranks and expands vector hits via graph paths
        """
        try:
            query = retrieval_data.get('query', '')
            query_embedding = retrieval_data.get('query_embedding')
            strategy = retrieval_data.get('strategy', 'hybrid')
            top_k = retrieval_data.get('top_k', 10)
            node_types = retrieval_data.get('node_types')
            
            # Perform graph-aware retrieval
            results = self.semantic_graph.enhanced_retrieval(
                query=query,
                query_embedding=query_embedding,
                strategy=strategy,
                top_k=top_k,
                node_types=node_types
            )
            
            # Log retrieval event
            retrieval_log = {
                'query': query,
                'strategy': strategy,
                'results_count': len(results.get('results', [])),
                'timestamp': datetime.now().isoformat()
            }
            
            self.semantic_graph.ingestion_engine.ingest_event(
                IngestionSource.RETRIEVAL_LOGS,
                retrieval_log,
                priority=1
            )
            
            self.integration_stats['retrieval_calls'] += 1
            
            return results
            
        except Exception as e:
            logger.error(f"Retrieval integration failed: {e}")
            return {'error': str(e), 'results': []}
    
    # Integration Point 5: Plan generation -> GraphAwarePlanning.generate_plan()
    def _handle_planning(self, planning_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook: Planner.create_plan()
        What Happens: Seeds tasks from high-importance graph neighborhoods
        """
        try:
            research_question = planning_data.get('research_question', '')
            context = planning_data.get('context', {})
            strategy = planning_data.get('strategy', 'hybrid')
            max_steps = planning_data.get('max_steps', 8)
            
            # Generate graph-aware plan
            plan = self.semantic_graph.enhanced_planning(
                research_question=research_question,
                context=context,
                strategy=strategy,
                max_steps=max_steps
            )
            
            # Log planning event
            planning_log = {
                'research_question': research_question,
                'strategy': strategy,
                'plan_steps': len(plan.get('plan_steps', [])),
                'graph_connectivity': plan.get('graph_connectivity', {}),
                'timestamp': datetime.now().isoformat()
            }
            
            self.semantic_graph.ingestion_engine.ingest_event(
                IngestionSource.PLANNER_OUTPUTS,
                planning_log,
                priority=2
            )
            
            self.integration_stats['plan_generations'] += 1
            
            return plan
            
        except Exception as e:
            logger.error(f"Planning integration failed: {e}")
            return {'error': str(e), 'plan_steps': []}
    
    # Integration Point 6: Preference logging -> GraphRLHFIntegration.record_preference()
    def _handle_preference(self, preference_data: Dict[str, Any]) -> str:
        """
        Hook: RLHFManager.log_preference()
        What Happens: Adds typed "Prefers" edges and detects reward-hacking patterns
        """
        try:
            user_id = preference_data.get('user_id', 'anonymous')
            preferred_content = preference_data.get('preferred_content', '')
            rejected_content = preference_data.get('rejected_content', '')
            feedback_type = preference_data.get('feedback_type', 'quality')
            confidence = preference_data.get('confidence', 1.0)
            context = preference_data.get('context', '')
            
            # Record preference in semantic graph
            preference_id = self.semantic_graph.record_user_feedback(
                user_id=user_id,
                preferred_content=preferred_content,
                rejected_content=rejected_content,
                feedback_type=feedback_type,
                confidence=confidence,
                context=context
            )
            
            self.integration_stats['preference_logs'] += 1
            
            return f"User preference recorded: {preference_id}"
            
        except Exception as e:
            logger.error(f"Preference logging integration failed: {e}")
            return f"Preference logging error: {str(e)}"
    
    # Integration Point 7: Monitoring -> GraphMonitor.record_metrics()
    def _handle_monitoring(self, monitoring_data: Dict[str, Any]) -> str:
        """
        Hook: AgentLifecycle.on_step_complete()
        What Happens: Emits node/edge stats and performance timing
        """
        try:
            step_name = monitoring_data.get('step_name', 'unknown')
            execution_time = monitoring_data.get('execution_time', 0.0)
            success = monitoring_data.get('success', True)
            metrics = monitoring_data.get('metrics', {})
            
            # Record operation timing
            self.semantic_graph.monitoring.record_operation_time(step_name, execution_time * 1000)
            
            # Record errors if any
            if not success:
                error_type = monitoring_data.get('error_type', 'general_error')
                self.semantic_graph.monitoring.record_error(error_type)
            
            # Log monitoring event
            monitoring_log = {
                'step_name': step_name,
                'execution_time': execution_time,
                'success': success,
                'metrics': metrics,
                'timestamp': datetime.now().isoformat()
            }
            
            self.semantic_graph.record_context_event(
                context_type='monitoring',
                content=f"Step: {step_name}, Time: {execution_time:.2f}s",
                relevance=0.3
            )
            
            self.integration_stats['monitoring_events'] += 1
            
            return f"Monitoring data recorded for step: {step_name}"
            
        except Exception as e:
            logger.error(f"Monitoring integration failed: {e}")
            return f"Monitoring integration error: {str(e)}"
    
    # Utility methods for research agent components
    
    def integrate_memory_manager(self, memory_manager):
        """Integrate with memory manager to capture writes"""
        original_save_method = memory_manager.save_research_finding
        
        def enhanced_save_finding(content: str, importance: float = 0.5, **kwargs):
            # Call original method
            result = original_save_method(content, importance, **kwargs)
            
            # Integrate with semantic graph
            memory_data = {
                'content': content,
                'importance': importance,
                'memory_type': 'research_finding',
                'session_id': getattr(memory_manager, 'current_episode_id', 'default'),
                **kwargs
            }
            self._handle_memory_output(memory_data)
            
            return result
        
        # Replace method
        memory_manager.save_research_finding = enhanced_save_finding
        logger.info("Memory manager integrated with semantic graph")
    
    def integrate_tool_executor(self, tool_executor):
        """Integrate with tool executor to capture usage"""
        original_invoke_method = tool_executor.invoke
        
        def enhanced_invoke(tool_input: Dict[str, Any]):
            start_time = datetime.now()
            
            try:
                # Call original method
                result = original_invoke_method(tool_input)
                success = True
                error = None
            except Exception as e:
                result = f"Tool execution failed: {str(e)}"
                success = False
                error = str(e)
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Integrate with semantic graph
            tool_data = {
                'tool_name': tool_input.get('tool', 'unknown'),
                'tool_input': str(tool_input.get('tool_input', '')),
                'tool_output': str(result),
                'execution_time': execution_time,
                'success': success,
                'error': error
            }
            self._handle_tool_usage(tool_data)
            
            if not success:
                raise Exception(error)
            
            return result
        
        # Replace method
        tool_executor.invoke = enhanced_invoke
        logger.info("Tool executor integrated with semantic graph")
    
    def integrate_research_loop(self, research_agent):
        """Integrate with research loop to capture findings"""
        original_execute_step = research_agent.execute_research_step
        
        def enhanced_execute_step(state):
            # Call original method
            result_state = original_execute_step(state)
            
            # Extract and integrate findings
            if 'findings' in result_state and result_state['findings']:
                latest_finding = result_state['findings'][-1]
                finding_data = {
                    'finding': latest_finding.get('analysis', ''),
                    'step_info': {
                        'step_number': latest_finding.get('step', 0),
                        'step_description': latest_finding.get('step_description', '')
                    },
                    'confidence': 0.7,  # Default confidence
                    'sources': latest_finding.get('external_research', []),
                    'analysis': latest_finding.get('analysis', '')
                }
                self._handle_finding(finding_data)
            
            return result_state
        
        # Replace method
        research_agent.execute_research_step = enhanced_execute_step
        logger.info("Research loop integrated with semantic graph")
    
    def integrate_rlhf_system(self, rlhf_system):
        """Integrate with RLHF system to capture preferences"""
        if hasattr(rlhf_system, 'feedback_collector') and rlhf_system.feedback_collector:
            original_capture_method = rlhf_system.feedback_collector.capture_research_output
            
            def enhanced_capture_output(research_result, research_question, session_id):
                # Call original method
                result = original_capture_method(research_result, research_question, session_id)
                
                # Integrate with semantic graph (this would be triggered by user feedback)
                # For now, we just log the capture event
                self.semantic_graph.record_context_event(
                    context_type='rlhf_capture',
                    content=f"Research output captured for feedback: {session_id}",
                    relevance=0.5
                )
                
                return result
            
            rlhf_system.feedback_collector.capture_research_output = enhanced_capture_output
            logger.info("RLHF system integrated with semantic graph")
    
    def get_integration_statistics(self) -> Dict[str, Any]:
        """Get comprehensive integration statistics"""
        semantic_stats = self.semantic_graph.get_comprehensive_stats()
        
        return {
            'integration_stats': self.integration_stats,
            'semantic_graph_stats': semantic_stats,
            'hooks_registered': len(self.integration_hooks),
            'total_integrations': sum(self.integration_stats.values()),
            'last_updated': datetime.now().isoformat()
        }
    
    def process_pending_events(self):
        """Process any pending ingestion events"""
        self.semantic_graph.process_pending_ingestion()
    
    def get_integration_health(self) -> Dict[str, Any]:
        """Get health status of integration points"""
        health_data = {
            'integration_points_active': len(self.integration_hooks),
            'total_events_processed': sum(self.integration_stats.values()),
            'semantic_graph_health': self.semantic_graph.get_monitoring_dashboard_data(),
            'integration_errors': 0,  # Could track errors per integration point
            'last_activity': datetime.now().isoformat()
        }
        
        # Determine overall health
        if health_data['total_events_processed'] > 0:
            health_data['status'] = 'active'
        else:
            health_data['status'] = 'idle'
        
        return health_data

# Factory function for easy integration
def create_ai_research_agent_integration(semantic_graph_agent: SemanticGraphAgent) -> AIResearchAgentIntegration:
    """Factory function to create AI research agent integration"""
    return AIResearchAgentIntegration(semantic_graph_agent)

# Integration helper for research agent
def integrate_research_agent_with_semantic_graph(research_agent, use_neo4j: bool = False, 
                                                neo4j_config: Optional[Dict[str, Any]] = None):
    """
    Complete integration helper that connects a research agent with semantic graph
    
    Args:
        research_agent: The research agent instance to integrate
        use_neo4j: Whether to use Neo4j backend
        neo4j_config: Neo4j configuration if using Neo4j
    
    Returns:
        AIResearchAgentIntegration: The integration instance
    """
    # Create semantic graph agent
    from .research_agent_integration import create_semantic_graph_agent
    semantic_graph_agent = create_semantic_graph_agent(use_neo4j, neo4j_config)
    
    # Create integration
    integration = create_ai_research_agent_integration(semantic_graph_agent)
    
    # Integrate all components
    if hasattr(research_agent, 'advanced_memory_tools'):
        # Find memory manager in tools
        for tool in research_agent.advanced_memory_tools:
            if hasattr(tool, 'func') and hasattr(tool.func, '__self__'):
                memory_manager = tool.func.__self__
                integration.integrate_memory_manager(memory_manager)
                break
    
    if hasattr(research_agent, 'tool_executor'):
        integration.integrate_tool_executor(research_agent.tool_executor)
    
    integration.integrate_research_loop(research_agent)
    
    if hasattr(research_agent, 'rlhf_enabled') and research_agent.rlhf_enabled:
        integration.integrate_rlhf_system(research_agent)
    
    logger.info("Complete research agent integration with semantic graph completed")
    
    return integration