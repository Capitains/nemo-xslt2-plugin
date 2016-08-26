<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs tei" version="2.0">

    <xsl:strip-space elements="*"/>
    <xsl:output method="html" indent="yes" omit-xml-declaration="yes" name="html"/>
    

    <xsl:template match="/">
        <xsl:apply-templates select="//tei:body"/>
    </xsl:template>

    <xsl:template match="tei:body">

        <article id="text" class="tab-pane active">
            <aside class="text-left">
                <div class="btn-group">
                    <button type="button" class="btn btn-success" id="fac"
                        >Facsimilaire</button>
                    <button type="button" class="btn btn-default" id="reg"
                        >Normalisée</button>
                </div>
            </aside>
            
            <xsl:apply-templates/>
            <footer class="row">
                <hr class="information-hr" title="notes de bas de page"/>
                <ul class="list-unstyled">
                    <xsl:apply-templates select="//tei:text//tei:witDetail" mode="notesbasdepage"/>
                </ul>
            </footer>
        </article>
    </xsl:template>

    <xsl:template match="tei:body/tei:div">
        <xsl:element name="div">
            <xsl:call-template name="id"/>
            <xsl:if test="./tei:head">
                <xsl:element name="h2"> 
                    <xsl:attribute name="class">reg</xsl:attribute>
                    <xsl:apply-templates select="./tei:head"/>
                    <xsl:text>&#160;</xsl:text> 
                </xsl:element>
            </xsl:if>
            <xsl:element name="div">
                <xsl:apply-templates select="./tei:div"/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
   
    <xsl:template match="tei:l">
        <xsl:element name="li">
            <xsl:attribute name="n">
                <xsl:value-of select="@n"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="tei:lg">
        <xsl:element name="ol">
            <xsl:attribute name="n">
                <xsl:value-of select="@n"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="tei:p">
        <xsl:element name="div">
            <xsl:attribute name="class">row</xsl:attribute>
            <xsl:if test="parent::tei:div[@n = '1']">
                <xsl:element name="span">
                    <xsl:attribute name="class">reg</xsl:attribute>
                    <xsl:value-of select="./ancestor::tei:div[@type = 'chapter']/@n"/>
                    <xsl:text>.&#160;</xsl:text>
                </xsl:element>
            </xsl:if>
            <xsl:apply-templates/>
        </xsl:element>

        <xsl:element name="br"/>
    </xsl:template>

    <!-- saut de page et de colonne + espace -->

    <xsl:template match="tei:lb">
        <xsl:element name="br">
            <xsl:attribute name="class">orig</xsl:attribute>
        </xsl:element>
    </xsl:template>

    <xsl:template match="tei:cb">
        <hr class="information-hr orig" title="Colonne {@n}"/>
        <span class="reg">
            <xsl:element name="span">
                <xsl:attribute name="class">reg</xsl:attribute>
                <xsl:element name="a">
                    <xsl:attribute name="href">
                        <xsl:value-of select="preceding::tei:pb[1]/@facs"/>
                    </xsl:attribute>
                    <xsl:text>&#160;[ fol. </xsl:text>
                    <xsl:value-of select="preceding::tei:pb[1]/@n"/>
                    <xsl:value-of select="@n"/>
                    <xsl:text>]&#160;</xsl:text>
                </xsl:element>
            </xsl:element>
        </span>
    </xsl:template>

    <xsl:template match="tei:pb">
        <hr class="information-hr orig" title="Folio {@n}" a="{@facs}"/>
        <a href="{@facs}" class="orig col-md-1 col-md-offset-10">
            <xsl:text>[fol.</xsl:text>
            <xsl:value-of select="@n"/>
            <xsl:text>]</xsl:text>
        </a>
        <br/>
    </xsl:template>

    <!-- fin saut de page et de colonne -->

    <!-- éléments à affichier pour la visualisation facsimilaire -->
    <xsl:template match="tei:orig">
        <xsl:element name="span">
            <xsl:attribute name="class">orig</xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="tei:abbr">
        <xsl:element name="span">
            <xsl:attribute name="class">abbr</xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="tei:pc[@type = 'orig']">
        <xsl:element name="span">
            <xsl:attribute name="class">orig</xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <!-- éléments de mise en page du manuscrit -->

    <xsl:template match="tei:rdg[@rend]">
        <xsl:element name="span">
            <xsl:attribute name="class">
                <xsl:value-of select="@rend"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="tei:hi[@rend]">
        <xsl:choose>
            <xsl:when test="./@rend = 'exp'">
                <xsl:element name="sup">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="span">
                    <xsl:attribute name="class">
                        <xsl:value-of select="@rend"/>
                    </xsl:attribute>
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="tei:add[@place]">

        <xsl:element name="span">
            <xsl:attribute name="class">
                <xsl:value-of select="@place"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>

    </xsl:template>
    <xsl:template match="tei:gap[@reason = 'lacuna']">
        <xsl:element name="span">
            <xsl:attribute name="class">
                <xsl:text>lacuna</xsl:text>
            </xsl:attribute>
            <xsl:text>            </xsl:text>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="tei:corr">
        <xsl:element name="span">
            <xsl:attribute name="class">
                <xsl:text>corr</xsl:text>
                <xsl:value-of select="@rend"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="tei:del">
        <xsl:element name="span">
            <xsl:attribute name="class">
                <xsl:text>del </xsl:text>
                <xsl:value-of select="@rend"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="tei:metamark">
        <span class="information-hr metamark" title="{@function}">
            <xsl:apply-templates/>
        </span>
    </xsl:template>
    <!-- fin de éléments de mise en page du manuscrit -->


    <!-- fin éléments à afficher pour la visualisation facsimilaire -->

    <!-- éléments à affichier pour la visualisation normalisée -->
    <xsl:template match="tei:reg">
        <xsl:element name="span">
            <xsl:attribute name="class">reg</xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="tei:corr">
        <xsl:element name="span">
            <xsl:attribute name="class">reg</xsl:attribute>
            <xsl:text>[</xsl:text>
            <xsl:apply-templates/>
            <xsl:text>]</xsl:text>
        </xsl:element>
    </xsl:template>
    <xsl:template match="tei:expan">
        <xsl:element name="span">
            <xsl:attribute name="class">expan</xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="tei:ex">
        <xsl:element name="span">
            <xsl:attribute name="style">
                <xsl:text>margin-left: 0;</xsl:text>
                <xsl:text>background-color:#ccc;</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="tei:pc[@type = 'reg']">
        <xsl:element name="span">
            <xsl:attribute name="class">reg</xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="tei:said">
        <xsl:element name="span">
            <xsl:attribute name="class">reg</xsl:attribute>
            <xsl:text>" </xsl:text>
        </xsl:element>
        <xsl:apply-templates/>
        <xsl:element name="span">
            <xsl:attribute name="class">reg</xsl:attribute>
            <xsl:text> "</xsl:text>
        </xsl:element>
    </xsl:template>

    <xsl:template match="tei:seg[@xml:lang = 'lat']">
        <xsl:element name="span">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="tei:seg[@type = 'number']">
        <xsl:element name="span">
            <xsl:attribute name="class">number</xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- fin éléments à affichier pour la visualisation normalisée -->

    <!-- fin édition mode visualisation par témoin -->

    <!-- Footer starts -->
    <xsl:template match="tei:body//tei:note">
        <xsl:variable name="pos">
            <xsl:number count="tei:note" level="any" from="tei:text"/>
        </xsl:variable>

        <xsl:variable name="infobulle" select="normalize-space(.)"/>
        <sup>
            <a name="appelnote{$pos}" href="#textenote{$pos}" title="{$infobulle}">
                <xsl:value-of select="$pos"/>
            </a>
        </sup>
    </xsl:template>


    <xsl:template match="tei:text//tei:note" mode="notesbasdepage">
        <xsl:variable name="pos">
            <xsl:number count="tei:text//tei:note" level="any" from="tei:text"/>
        </xsl:variable>
        <li>
            <a name="textenote{$pos}" href="#appelnote{$pos}">
                <xsl:value-of select="$pos"/>
            </a>
            <xsl:text> </xsl:text>
            <xsl:value-of select="."/>
        </li>
    </xsl:template>

    <xsl:template match="tei:editionStmt">
        <p style="font-size:small">
            <xsl:apply-templates/>
        </p>
    </xsl:template>

    <xsl:template match="tei:publicationStmt">
        <p style="font-size:small;">
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    <!-- Header ends -->

    <!-- templates -->
    <!-- règles de numérotation des vers -->

    <!--     <xsl:template name="ol">
        <xsl:element name="ol">
            <xsl:attribute name="start">
                <xsl:value-of select="./tei:l[1]/@n"/>
            </xsl:attribute>
            <xsl:attribute name="class">
                <xsl:text>norm</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    
    -->

    <!-- attribution des id -->
    <xsl:template name="id">
        <xsl:attribute name="id">
            <xsl:value-of select="@type"/>

            <xsl:value-of select="@n"/>

        </xsl:attribute>
    </xsl:template>
</xsl:stylesheet>
