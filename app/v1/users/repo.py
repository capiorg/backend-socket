class UserRepository:
    def __init__(self, db_session: sessionmaker):
        # super().__init__(db_session=db_session)
        self.session = db_session
        self.model = Contract

        self.base = BaseCRUD(db_session=db_session, model=self.model)
