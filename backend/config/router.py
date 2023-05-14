from django.conf import settings


class ShardDBRouter:
    databases = settings.DATABASES
    route_app_labels = {"user"}

    def db_for_read(self, model, **hints):
        """
        모델 인스턴스의 읽기 작업에 대해 사용할 데이터베이스를 반환한다.
        model은 쿼리가 수행되는 모델 클래스이며, hints는 선택적이다.
        읽기 작업에 대해 각 모델 클래스가 사용할 데이터베이스를 반환할 수 있다.
        => app 단(or model) 에서 샤딩이 필요 할 경우 분기 처리 할 수 있을 듯!
        """
        db_name = "default"
        return db_name

    def db_for_write(self, model, **hints):
        """
        모델 인스턴스의 쓰기 작업에 대해 사용할 데이터베이스를 반환한다.
        모델 클래스가 쓰기 작업에 대해 사용할 데이터베이스를 반환할 수 있습니다.
        => 이 역시도 app 단(or model) 에서 샤딩이 필요 할 경우 분기 처리에 사용
        """

        db_name = "default"
        return db_name

    @staticmethod
    def allow_relation(obj1, obj2, **hints):
        """
        두 개의 모델 인스턴스 obj1과 obj2가 상호 작용할 수 있는지 여부를 판단하고
        모델 클래스 간에 관계를 허용할 수 있는지 여부를 결정한다.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        지정된 데이터베이스 db에서 app_label 애플리케이션의 model_name 모델의 마이그레이션을 수행할 수 있는지 여부를 결정한다.
        => 이 과정을 잘 사용하면 DB 내용변경에 있어서 검증에 대한 로직도 구현할 수 있을듯?!
        model_name은 선택적으로 지정가능.
        """
        migrate = False
        if app_label in self.route_app_labels:
            # shard_1, shard_2에서 모두 migration을 허용.
            if db in ["shard_1", "shard_2"]:
                migrate = True
        return migrate
