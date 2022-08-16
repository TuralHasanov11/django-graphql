from unicodedata import category
import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Quiz, Category, Question, Answer


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id","name")

class QuizType(DjangoObjectType):
    class Meta:
        model = Quiz
        fields = ("id","title","category","quiz")

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title","quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question","answer_text")

class Query(graphene.ObjectType):

    all_quizzes = graphene.List(QuizType)
    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    def resolve_all_quizzes(root, info):
        return Quiz.objects.all()
    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)
    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)

class CategoryCreateMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryCreateMutation(category=category)

class CategoryUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name):
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()
        return CategoryUpdateMutation(category=category)

class CategoryDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(pk=id)
        category.delete()
        return id

class Mutation(graphene.ObjectType):
    create_category = CategoryCreateMutation.Field()
    update_category = CategoryUpdateMutation.Field()
    delete_category = CategoryDeleteMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)