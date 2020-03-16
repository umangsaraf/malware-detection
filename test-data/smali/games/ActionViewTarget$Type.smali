.class public final enum Lcom/espian/showcaseview/ActionViewTarget$Type;
.super Ljava/lang/Enum;
.source "ActionViewTarget.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/espian/showcaseview/ActionViewTarget;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x4019
    name = "Type"
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Ljava/lang/Enum",
        "<",
        "Lcom/espian/showcaseview/ActionViewTarget$Type;",
        ">;"
    }
.end annotation


# static fields
.field private static final synthetic ENUM$VALUES:[Lcom/espian/showcaseview/ActionViewTarget$Type;

.field public static final enum HOME:Lcom/espian/showcaseview/ActionViewTarget$Type;

.field public static final enum OVERFLOW:Lcom/espian/showcaseview/ActionViewTarget$Type;

.field public static final enum SPINNER:Lcom/espian/showcaseview/ActionViewTarget$Type;

.field public static final enum TITLE:Lcom/espian/showcaseview/ActionViewTarget$Type;


# direct methods
.method static constructor <clinit>()V
    .locals 6

    .prologue
    const/4 v5, 0x3

    const/4 v4, 0x2

    const/4 v3, 0x1

    const/4 v2, 0x0

    .line 54
    new-instance v0, Lcom/espian/showcaseview/ActionViewTarget$Type;

    const-string v1, "SPINNER"

    invoke-direct {v0, v1, v2}, Lcom/espian/showcaseview/ActionViewTarget$Type;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/espian/showcaseview/ActionViewTarget$Type;->SPINNER:Lcom/espian/showcaseview/ActionViewTarget$Type;

    new-instance v0, Lcom/espian/showcaseview/ActionViewTarget$Type;

    const-string v1, "HOME"

    invoke-direct {v0, v1, v3}, Lcom/espian/showcaseview/ActionViewTarget$Type;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/espian/showcaseview/ActionViewTarget$Type;->HOME:Lcom/espian/showcaseview/ActionViewTarget$Type;

    new-instance v0, Lcom/espian/showcaseview/ActionViewTarget$Type;

    const-string v1, "TITLE"

    invoke-direct {v0, v1, v4}, Lcom/espian/showcaseview/ActionViewTarget$Type;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/espian/showcaseview/ActionViewTarget$Type;->TITLE:Lcom/espian/showcaseview/ActionViewTarget$Type;

    new-instance v0, Lcom/espian/showcaseview/ActionViewTarget$Type;

    const-string v1, "OVERFLOW"

    invoke-direct {v0, v1, v5}, Lcom/espian/showcaseview/ActionViewTarget$Type;-><init>(Ljava/lang/String;I)V

    sput-object v0, Lcom/espian/showcaseview/ActionViewTarget$Type;->OVERFLOW:Lcom/espian/showcaseview/ActionViewTarget$Type;

    .line 53
    const/4 v0, 0x4

    new-array v0, v0, [Lcom/espian/showcaseview/ActionViewTarget$Type;

    sget-object v1, Lcom/espian/showcaseview/ActionViewTarget$Type;->SPINNER:Lcom/espian/showcaseview/ActionViewTarget$Type;

    aput-object v1, v0, v2

    sget-object v1, Lcom/espian/showcaseview/ActionViewTarget$Type;->HOME:Lcom/espian/showcaseview/ActionViewTarget$Type;

    aput-object v1, v0, v3

    sget-object v1, Lcom/espian/showcaseview/ActionViewTarget$Type;->TITLE:Lcom/espian/showcaseview/ActionViewTarget$Type;

    aput-object v1, v0, v4

    sget-object v1, Lcom/espian/showcaseview/ActionViewTarget$Type;->OVERFLOW:Lcom/espian/showcaseview/ActionViewTarget$Type;

    aput-object v1, v0, v5

    sput-object v0, Lcom/espian/showcaseview/ActionViewTarget$Type;->ENUM$VALUES:[Lcom/espian/showcaseview/ActionViewTarget$Type;

    return-void
.end method

.method private constructor <init>(Ljava/lang/String;I)V
    .locals 0

    .prologue
    .line 53
    invoke-direct {p0, p1, p2}, Ljava/lang/Enum;-><init>(Ljava/lang/String;I)V

    return-void
.end method

.method public static valueOf(Ljava/lang/String;)Lcom/espian/showcaseview/ActionViewTarget$Type;
    .locals 1

    .prologue
    .line 1
    const-class v0, Lcom/espian/showcaseview/ActionViewTarget$Type;

    invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;

    move-result-object v0

    check-cast v0, Lcom/espian/showcaseview/ActionViewTarget$Type;

    return-object v0
.end method

.method public static values()[Lcom/espian/showcaseview/ActionViewTarget$Type;
    .locals 4

    .prologue
    const/4 v3, 0x0

    .line 1
    sget-object v0, Lcom/espian/showcaseview/ActionViewTarget$Type;->ENUM$VALUES:[Lcom/espian/showcaseview/ActionViewTarget$Type;

    array-length v1, v0

    new-array v2, v1, [Lcom/espian/showcaseview/ActionViewTarget$Type;

    invoke-static {v0, v3, v2, v3, v1}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    return-object v2
.end method
