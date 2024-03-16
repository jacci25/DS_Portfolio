## DATA422 Group Project
## Date: 20/10/23
## Author: Jacci, Sarah, Emma and Levo

function(input, output, session) {
  
  # Scatter plot for the entirety of NZ
  output$trend_plot <- renderPlotly({
    ggplotly(ggplot(map_df, aes(x=V_P_100, y=Price, colour=S_P_100, text=paste("TA:", TA2023_V_2))) +
               geom_point(alpha=0.5) +
               scale_colour_gradientn(colours = terrain.colors(10)) +
               labs(color = "Number of Schools per 10,000 inhabitants" ) +
               ggtitle("Impact of Crime Rate and Number of Schools on Housing Price") +
               ylab("Average Housing Price") +
               xlab("Number of Victimizations per 10,000 inhabitants") +
               theme_minimal())
  })
  
  
  # Choropleth maps for average house price, school and crime data
  observe(
    input$data_map
  )
  output$map <- renderLeaflet({
    d <- input$data_map
    pal <- colorNumeric("YlOrRd", map_df[[d]]) 
    
    if (input$data_map == "Price")({
      leg_title <- "Average house price"
      leg_pref <- "$"
    })
    if (input$data_map == "S_P_100")({
      leg_title <- "Number of schools per 10,000 inhabitants"
      leg_pref <- ""
    })
    if (input$data_map == "V_P_100")({
      leg_title <- "Crime rate per 10,000 inhabitants"
      leg_pref <- ""
    })
    
    
    leaflet(map_df) %>%
      setView(lng=174, lat=-41, zoom=5) %>%
      addTiles() %>%
      addPolygons(layerId = ~TA2023_V_2,
                  color = "white",
                  weight = 2, 
                  smoothFactor = 0.5,
                  opacity = 1, 
                  fillOpacity = 0.7,
                  fillColor = ~pal(map_df[[d]]),
                  dashArray = "3",
                  highlightOptions = highlightOptions(
                    weight = 5,
                    color = "#666",
                    dashArray = "",
                    fillOpacity = 0.7,
                    bringToFront = TRUE),
                  label = ~TA2023_V_2
      ) %>%
      addLegend("bottomright", pal = pal, values = ~map_df[[d]],
                title = leg_title,
                labFormat = labelFormat(prefix = leg_pref),
                opacity = 0.7)
  })
  
  # Territorial authority specifc bar charts (appear on user selection)
  observeEvent(input$map_shape_click, {
    
    click <- input$map_shape_click
    
    selected_df <- df[df$Territorial_Authority == click$id,]
    selected_crime <- crime_df[crime_df$Territorial_Authority == click$id,]
    selected_school <- school_df[school_df$Territorial_Authority == click$id,] 
    
    # If click id isn't null, render plots
    if(!is.null(click$id) & click$id != 'Area Outside Territorial Authority'){
      output$detail_title <- renderText({
        sprintf("Crime rate and school details for %s", click$id)
      })
      # Crime bar chart
      output$crime <- renderPlotly({
        ggplot(selected_crime, aes(Anzsoc_Division, Total_Victimisations, fill=Anzsoc_Division)) +
          geom_col() +
          scale_x_discrete(labels = function(x) stringr::str_wrap(x, width = 20)) +
          xlab(NULL)+
          ggtitle(paste("Crime rate in", click$id, "(01.2023 - 06.2023)")) +
          theme_minimal() +
          theme(legend.title = element_blank()) + 
          theme(legend.position='none') +
          scale_fill_brewer(palette="Set3")
      })
      # School bar chart
      output$school <- renderPlotly({
        ggplot(selected_school, aes(School_Type, School_Count, fill=School_Type), show.legend = FALSE) +
          geom_col() +
          scale_x_discrete(labels = function(x) stringr::str_wrap(x, width = 15)) +
          xlab(NULL) +
          ggtitle(paste("Number of schools in", click$id)) +
          theme_minimal() +
          theme(legend.title = element_blank()) + 
          theme(legend.position='none') +
          scale_fill_brewer(palette="Set3")
      })
  }
})
}
