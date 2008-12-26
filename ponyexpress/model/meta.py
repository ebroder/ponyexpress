# SQLAlchemy database engine.  Updated by model.init_model()
engine = None

# SQLAlchemy session manager.  Updated by model.init_model()
Session = None

__all__ = ['engine', 'Session']
