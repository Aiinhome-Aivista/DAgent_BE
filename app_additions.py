# ============================================================
# app.py ADDITIONS — paste these into your existing app.py
# ============================================================
#
# 1. Add these imports at the top of app.py (after existing imports):
#
# from controllers.workspace_data_processor import (
#     workspace_process_sources_controller,
#     workspace_source_status_controller,
# )
# from controllers.session_insights_controller import (
#     session_insights_controller,
# )
# from controllers.session_analysis_controller_v2 import (
#     session_analysis_controller_v2,
#     session_analysis_history_controller,
# )
# from controllers.session_chat_history_controller_v2 import (
#     session_chat_history_controller_v2,
# )
#
#
# 2. Replace or add these routes in app.py:
# ============================================================

# ── Workspace: process all data sources (delta-only) ──────────────────────────

# @app.route("/workspace/process-sources", methods=["POST"])
# def workspace_process_sources():
#     """
#     Process ALL data sources for a workspace session.
#     Uses content hashing to skip unchanged files — only re-processes
#     files / tables that have actually changed.
#     """
#     return workspace_process_sources_controller(get_db_connection)

# @app.route("/workspace/source-status", methods=["GET"])
# def workspace_source_status():
#     """
#     Returns the current registry status for all data sources
#     in a workspace (processed / skipped / error).
#     """
#     return workspace_source_status_controller(get_db_connection)


# ── Session Analysis (v2 — saves per user, delta-aware) ───────────────────────

# @app.route("/session-analysis", methods=["POST"])
# def session_analysis():
#     """
#     Analyse all workspace data sources together.
#     Saves results into session_analysis_results (per user).
#     Returns from_cache=true if data unchanged since last run.
#     """
#     return session_analysis_controller_v2(get_db_connection)

# @app.route("/session-analysis/history", methods=["GET"])
# def session_analysis_history():
#     """
#     Returns all saved analysis results for a workspace session+user.
#     """
#     return session_analysis_history_controller(get_db_connection)


# ── Chat History (v2 — stores visualizations, named groups) ───────────────────

# @app.route("/session-chat-history", methods=["GET", "POST", "DELETE"])
# def session_chat_history():
#     """
#     GET    → list all Q&A turns grouped by chat_id (named conversation groups)
#     POST   → save a new Q&A turn (includes visualizations)
#     DELETE → delete all or a specific chat group
#     """
#     return session_chat_history_controller_v2(get_db_connection)


# ── Saved Insights (pin analysis / chat / visualizations) ─────────────────────

# @app.route("/session-insights", methods=["GET", "POST"])
# def session_insights():
#     return session_insights_controller(get_db_connection)

# @app.route("/session-insights/<int:insight_id>", methods=["DELETE"])
# def delete_session_insight(insight_id):
#     return session_insights_controller(get_db_connection, insight_id=insight_id)


# ── IMPORTANT ──────────────────────────────────────────────────────────────────
# The existing /session-analysis and /session-chat-history routes should be
# REPLACED with the new v2 versions above.
#
# The existing session_analysis_controller and session_chat_history_controller
# can remain as fallbacks — just make sure the new routes are registered AFTER
# the old ones so Flask uses the newer handlers.
#
# Or simply comment out the old route registrations and uncomment the new ones.
# ──────────────────────────────────────────────────────────────────────────────
