<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns="http://www.w3.org/1999/xhtml">
 
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
 
  <xsl:template match="/url">
    <html>
      <head> <title>{{ title }}</title> </head>
      <body>
        <h1>{{ heading }}</h1>
        <div class="user">
        
          <div class="url">
          
          <abbr>
           <xsl:attribute name="class">date-added</xsl:attribute>
           <xsl:attribute name="title"><xsl:value-of select="date_added" /></xsl:attribute>
           <xsl:value-of select="date_added" />
          </abbr>
          <a>
           <xsl:attribute name="rel">source</xsl:attribute>
           <xsl:attribute name="href"><xsl:value-of select="source" /></xsl:attribute>
          </a>
          <ul>Categories
            <xsl:apply-templates select="categories">
              <xsl:sort select="category" />
            </xsl:apply-templates>          
          </ul>
          </div>
        
        </div>
      </body>
    </html>
  </xsl:template>
 
  <xsl:template match="category">
    <li class="category">
     <a>
      <xsl:attribute name="href"><xsl:value-of select="source" /></xsl:attribute>
      <xsl:attribute name="rel">category</xsl:attribute><xsl:value-of select="name"/>
     </a>
    </li>
  </xsl:template>
 
 
</xsl:stylesheet>