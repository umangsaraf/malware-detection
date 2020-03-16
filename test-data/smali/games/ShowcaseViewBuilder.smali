.class public Lcom/espian/showcaseview/ShowcaseViewBuilder;
.super Ljava/lang/Object;
.source "ShowcaseViewBuilder.java"


# instance fields
.field private final showcaseView:Lcom/espian/showcaseview/ShowcaseView;


# direct methods
.method public constructor <init>(Landroid/app/Activity;)V
    .locals 1
    .param p1, "activity"    # Landroid/app/Activity;

    .prologue
    .line 10
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 11
    new-instance v0, Lcom/espian/showcaseview/ShowcaseView;

    invoke-direct {v0, p1}, Lcom/espian/showcaseview/ShowcaseView;-><init>(Landroid/content/Context;)V

    iput-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    .line 12
    return-void
.end method

.method public constructor <init>(Landroid/app/Activity;I)V
    .locals 2
    .param p1, "activity"    # Landroid/app/Activity;
    .param p2, "showcaseLayoutViewId"    # I

    .prologue
    .line 18
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 19
    invoke-virtual {p1}, Landroid/app/Activity;->getLayoutInflater()Landroid/view/LayoutInflater;

    move-result-object v0

    const/4 v1, 0x0

    invoke-virtual {v0, p2, v1}, Landroid/view/LayoutInflater;->inflate(ILandroid/view/ViewGroup;)Landroid/view/View;

    move-result-object v0

    check-cast v0, Lcom/espian/showcaseview/ShowcaseView;

    iput-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    .line 20
    return-void
.end method

.method public constructor <init>(Lcom/espian/showcaseview/ShowcaseView;)V
    .locals 0
    .param p1, "showcaseView"    # Lcom/espian/showcaseview/ShowcaseView;

    .prologue
    .line 14
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 15
    iput-object p1, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    .line 16
    return-void
.end method


# virtual methods
.method public animateGesture(FFFF)Lcom/espian/showcaseview/ShowcaseViewBuilder;
    .locals 1
    .param p1, "offsetStartX"    # F
    .param p2, "offsetStartY"    # F
    .param p3, "offsetEndX"    # F
    .param p4, "offsetEndY"    # F

    .prologue
    .line 53
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    invoke-virtual {v0, p1, p2, p3, p4}, Lcom/espian/showcaseview/ShowcaseView;->animateGesture(FFFF)V

    .line 54
    return-object p0
.end method

.method public build()Lcom/espian/showcaseview/ShowcaseView;
    .locals 1

    .prologue
    .line 88
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    return-object v0
.end method

.method public overrideButtonClick(Landroid/view/View$OnClickListener;)Lcom/espian/showcaseview/ShowcaseViewBuilder;
    .locals 1
    .param p1, "listener"    # Landroid/view/View$OnClickListener;

    .prologue
    .line 48
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    invoke-virtual {v0, p1}, Lcom/espian/showcaseview/ShowcaseView;->overrideButtonClick(Landroid/view/View$OnClickListener;)V

    .line 49
    return-object p0
.end method

.method public pointTo(FF)Lcom/espian/showcaseview/ShowcaseViewBuilder;
    .locals 1
    .param p1, "x"    # F
    .param p2, "y"    # F

    .prologue
    .line 78
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    invoke-virtual {v0, p1, p2}, Lcom/espian/showcaseview/ShowcaseView;->pointTo(FF)V

    .line 79
    return-object p0
.end method

.method public pointTo(Landroid/view/View;)Lcom/espian/showcaseview/ShowcaseViewBuilder;
    .locals 1
    .param p1, "view"    # Landroid/view/View;

    .prologue
    .line 73
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    invoke-virtual {v0, p1}, Lcom/espian/showcaseview/ShowcaseView;->pointTo(Landroid/view/View;)V

    .line 74
    return-object p0
.end method

.method public setConfigOptions(Lcom/espian/showcaseview/ShowcaseView$ConfigOptions;)Lcom/espian/showcaseview/ShowcaseViewBuilder;
    .locals 1
    .param p1, "configOptions"    # Lcom/espian/showcaseview/ShowcaseView$ConfigOptions;

    .prologue
    .line 83
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    invoke-virtual {v0, p1}, Lcom/espian/showcaseview/ShowcaseView;->setConfigOptions(Lcom/espian/showcaseview/ShowcaseView$ConfigOptions;)V

    .line 84
    return-object p0
.end method

.method public setShowcaseIndicatorScale(F)Lcom/espian/showcaseview/ShowcaseViewBuilder;
    .locals 1
    .param p1, "scale"    # F

    .prologue
    .line 43
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    invoke-virtual {v0, p1}, Lcom/espian/showcaseview/ShowcaseView;->setShowcaseIndicatorScale(F)V

    .line 44
    return-object p0
.end method

.method public setShowcaseItem(IILandroid/app/Activity;)Lcom/espian/showcaseview/ShowcaseViewBuilder;
    .locals 1
    .param p1, "itemType"    # I
    .param p2, "actionItemId"    # I
    .param p3, "activity"    # Landroid/app/Activity;

    .prologue
    .line 38
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    invoke-virtual {v0, p1, p2, p3}, Lcom/espian/showcaseview/ShowcaseView;->setShowcaseItem(IILandroid/app/Activity;)V

    .line 39
    return-object p0
.end method

.method public setShowcaseNoView()Lcom/espian/showcaseview/ShowcaseViewBuilder;
    .locals 1

    .prologue
    .line 23
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    invoke-virtual {v0}, Lcom/espian/showcaseview/ShowcaseView;->setShowcaseNoView()V

    .line 24
    return-object p0
.end method

.method public setShowcasePosition(II)Lcom/espian/showcaseview/ShowcaseViewBuilder;
    .locals 1
    .param p1, "x"    # I
    .param p2, "y"    # I

    .prologue
    .line 33
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    invoke-virtual {v0, p1, p2}, Lcom/espian/showcaseview/ShowcaseView;->setShowcasePosition(II)V

    .line 34
    return-object p0
.end method

.method public setShowcaseView(Landroid/view/View;)Lcom/espian/showcaseview/ShowcaseViewBuilder;
    .locals 1
    .param p1, "view"    # Landroid/view/View;

    .prologue
    .line 28
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    invoke-virtual {v0, p1}, Lcom/espian/showcaseview/ShowcaseView;->setShowcaseView(Landroid/view/View;)V

    .line 29
    return-object p0
.end method

.method public setText(II)Lcom/espian/showcaseview/ShowcaseViewBuilder;
    .locals 1
    .param p1, "titleText"    # I
    .param p2, "subText"    # I

    .prologue
    .line 68
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    invoke-virtual {v0, p1, p2}, Lcom/espian/showcaseview/ShowcaseView;->setText(II)V

    .line 69
    return-object p0
.end method

.method public setText(Ljava/lang/String;Ljava/lang/String;)Lcom/espian/showcaseview/ShowcaseViewBuilder;
    .locals 1
    .param p1, "titleText"    # Ljava/lang/String;
    .param p2, "subText"    # Ljava/lang/String;

    .prologue
    .line 63
    iget-object v0, p0, Lcom/espian/showcaseview/ShowcaseViewBuilder;->showcaseView:Lcom/espian/showcaseview/ShowcaseView;

    invoke-virtual {v0, p1, p2}, Lcom/espian/showcaseview/ShowcaseView;->setText(Ljava/lang/String;Ljava/lang/String;)V

    .line 64
    return-object p0
.end method
