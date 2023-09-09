# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class NtBoard(models.Model):
    nt_board_idx = models.AutoField(db_column='NT_BOARD_IDX', primary_key=True)  # Field name made lowercase.
    nt_board_type = models.CharField(db_column='NT_BOARD_TYPE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    nt_board_subject = models.CharField(db_column='NT_BOARD_SUBJECT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nt_board_contents = models.TextField(db_column='NT_BOARD_CONTENTS', blank=True, null=True)  # Field name made lowercase.
    nt_board_cocktail = models.CharField(db_column='NT_BOARD_COCKTAIL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nt_board_thumbnail = models.FileField(db_column='NT_BOARD_THUMBNAIL', upload_to='column_thumbnail/', blank=True, null=True)  # Field name made lowercase.
    nt_board_dt = models.DateTimeField(db_column='NT_BOARD_DT', blank=True, null=True)  # Field name made lowercase.
    nt_board_main_yn = models.CharField(db_column='NT_BOARD_MAIN_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nt_board_delete_yn = models.CharField(db_column='NT_BOARD_DELETE_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nt_user_idx_fk = models.ForeignKey('NtUser', models.DO_NOTHING, db_column='NT_USER_IDX_FK', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NT_BOARD'


class NtBoardComment(models.Model):
    nt_board_comment_idx = models.AutoField(db_column='NT_BOARD_COMMENT_IDX', primary_key=True)  # Field name made lowercase.
    nt_board_comment_text = models.TextField(db_column='NT_BOARD_COMMENT_TEXT', blank=True, null=True)  # Field name made lowercase.
    nt_board_comment_dt = models.DateTimeField(db_column='NT_BOARD_COMMENT_DT', blank=True, null=True)  # Field name made lowercase.
    nt_board_idx_fk = models.ForeignKey(NtBoard, models.DO_NOTHING, db_column='NT_BOARD_IDX_FK', blank=True, null=True)  # Field name made lowercase.
    nt_user_idx_fk = models.ForeignKey('NtUser', models.DO_NOTHING, db_column='NT_USER_IDX_FK', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NT_BOARD_COMMENT'


class NtCocktail(models.Model):
    nt_cocktail_idx = models.AutoField(db_column='NT_COCKTAIL_IDX', primary_key=True)  # Field name made lowercase.
    nt_cocktail_nm = models.CharField(db_column='NT_COCKTAIL_NM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nt_cocktail_engnm = models.CharField(db_column='NT_COCKTAIL_ENGNM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nt_cocktail_recipe = models.TextField(db_column='NT_COCKTAIL_RECIPE', blank=True, null=True)  # Field name made lowercase.
    nt_cocktail_thumbnail = models.CharField(db_column='NT_COCKTAIL_THUMBNAIL', max_length=200, blank=True, null=True)  # Field name made lowercase.
    nt_cocktail_memo = models.CharField(db_column='NT_COCKTAIL_MEMO', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NT_COCKTAIL'


class NtCocktailComment(models.Model):
    nt_cocktail_comment_idx = models.AutoField(db_column='NT_COCKTAIL_COMMENT_IDX', primary_key=True)  # Field name made lowercase.
    nt_cocktail_comment_text = models.TextField(db_column='NT_COCKTAIL_COMMENT_TEXT', blank=True, null=True)  # Field name made lowercase.
    nt_cocktail_comment_dt = models.DateTimeField(db_column='NT_COCKTAIL_COMMENT_DT', blank=True, null=True)  # Field name made lowercase.
    nt_cocktail_idx_fk = models.ForeignKey(NtCocktail, models.DO_NOTHING, db_column='NT_COCKTAIL_IDX_FK', blank=True, null=True)  # Field name made lowercase.
    nt_user_idx_fk = models.ForeignKey('NtUser', models.DO_NOTHING, db_column='NT_USER_IDX_FK', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NT_COCKTAIL_COMMENT'


class NtCocktailRecipe(models.Model):
    nt_cocktail_idx_fk = models.OneToOneField(NtCocktail, models.DO_NOTHING, db_column='NT_COCKTAIL_IDX_FK', primary_key=True)  # Field name made lowercase. The composite primary key (NT_COCKTAIL_IDX_FK, NT_INGRDNT_IDX_FK) found, that is not supported. The first column is selected.
    nt_ingrdnt_idx_fk = models.ForeignKey('NtIngrdnt', models.DO_NOTHING, db_column='NT_INGRDNT_IDX_FK')  # Field name made lowercase.
    nt_cocktail_recipe_amt = models.CharField(db_column='NT_COCKTAIL_RECIPE_AMT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nt_cocktail_recipe_unit = models.CharField(db_column='NT_COCKTAIL_RECIPE_UNIT', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NT_COCKTAIL_RECIPE'
        unique_together = (('nt_cocktail_idx_fk', 'nt_ingrdnt_idx_fk'),)


class NtIngrdnt(models.Model):
    nt_ingrdnt_idx = models.AutoField(db_column='NT_INGRDNT_IDX', primary_key=True)  # Field name made lowercase.
    nt_ingrdnt_type = models.CharField(db_column='NT_INGRDNT_TYPE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    nt_ingrdnt_nm = models.CharField(db_column='NT_INGRDNT_NM', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NT_INGRDNT'


class NtUser(models.Model):
    nt_user_idx = models.AutoField(db_column='NT_USER_IDX', primary_key=True)  # Field name made lowercase.
    nt_user_id = models.CharField(db_column='NT_USER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nt_user_pw = models.CharField(db_column='NT_USER_PW', max_length=64, blank=True, null=True)  # Field name made lowercase.
    nt_user_email = models.CharField(db_column='NT_USER_EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nt_user_nickname = models.CharField(db_column='NT_USER_NICKNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nt_user_admin_yn = models.CharField(db_column='NT_USER_ADMIN_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NT_USER'


class NtUserIngrdnt(models.Model):
    nt_user_idx_fk = models.OneToOneField(NtUser, models.DO_NOTHING, db_column='NT_USER_IDX_FK', primary_key=True)  # Field name made lowercase. The composite primary key (NT_USER_IDX_FK, NT_INGRDNT_IDX_FK) found, that is not supported. The first column is selected.
    nt_ingrdnt_idx_fk = models.ForeignKey(NtIngrdnt, models.DO_NOTHING, db_column='NT_INGRDNT_IDX_FK')  # Field name made lowercase.
    nt_user_ingrdnt_amt = models.CharField(db_column='NT_USER_INGRDNT_AMT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nt_user_ingrdnt_unit = models.CharField(db_column='NT_USER_INGRDNT_UNIT', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NT_USER_INGRDNT'
        unique_together = (('nt_user_idx_fk', 'nt_ingrdnt_idx_fk'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'