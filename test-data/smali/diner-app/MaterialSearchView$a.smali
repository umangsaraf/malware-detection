.class public Lcom/miguelcatalan/materialsearchview/MaterialSearchView$a;
.super Ljava/lang/Object;
.source "MaterialSearchView.java"

# interfaces
.implements Landroid/view/View$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/miguelcatalan/materialsearchview/MaterialSearchView;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x1
    name = null
.end annotation


# instance fields
.field public final synthetic b:Lcom/miguelcatalan/materialsearchview/MaterialSearchView;


# direct methods
.method public constructor <init>(Lcom/miguelcatalan/materialsearchview/MaterialSearchView;)V
    .locals 0

    .line 1
    iput-object p1, p0, Lcom/miguelcatalan/materialsearchview/MaterialSearchView$a;->b:Lcom/miguelcatalan/materialsearchview/MaterialSearchView;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/view/View;)V
    .locals 2

    .line 1
    iget-object v0, p0, Lcom/miguelcatalan/materialsearchview/MaterialSearchView$a;->b:Lcom/miguelcatalan/materialsearchview/MaterialSearchView;

    .line 2
    iget-object v1, v0, Lcom/miguelcatalan/materialsearchview/MaterialSearchView;->j:Landroid/widget/ImageButton;

    if-ne p1, v1, :cond_0

    .line 3
    invoke-virtual {v0}, Lcom/miguelcatalan/materialsearchview/MaterialSearchView;->a()V

    goto :goto_0

    .line 4
    :cond_0
    iget-object v1, v0, Lcom/miguelcatalan/materialsearchview/MaterialSearchView;->k:Landroid/widget/ImageButton;

    if-ne p1, v1, :cond_1

    .line 5
    invoke-virtual {v0}, Lcom/miguelcatalan/materialsearchview/MaterialSearchView;->e()V

    goto :goto_0

    .line 6
    :cond_1
    iget-object v1, v0, Lcom/miguelcatalan/materialsearchview/MaterialSearchView;->l:Landroid/widget/ImageButton;

    if-ne p1, v1, :cond_2

    .line 7
    iget-object p1, v0, Lcom/miguelcatalan/materialsearchview/MaterialSearchView;->i:Landroid/widget/EditText;

    const/4 v0, 0x0

    .line 8
    invoke-virtual {p1, v0}, Landroid/widget/EditText;->setText(Ljava/lang/CharSequence;)V

    goto :goto_0

    .line 9
    :cond_2
    iget-object v1, v0, Lcom/miguelcatalan/materialsearchview/MaterialSearchView;->i:Landroid/widget/EditText;

    if-ne p1, v1, :cond_3

    .line 10
    invoke-virtual {v0}, Lcom/miguelcatalan/materialsearchview/MaterialSearchView;->g()V

    goto :goto_0

    .line 11
    :cond_3
    iget-object v1, v0, Lcom/miguelcatalan/materialsearchview/MaterialSearchView;->g:Landroid/view/View;

    if-ne p1, v1, :cond_4

    .line 12
    invoke-virtual {v0}, Lcom/miguelcatalan/materialsearchview/MaterialSearchView;->a()V

    :cond_4
    :goto_0
    return-void
.end method
