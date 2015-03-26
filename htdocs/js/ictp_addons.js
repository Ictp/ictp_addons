
function createDeleteAllDialog(timetable){
    var txt = "<p>Are you sure you wish to delete ALL sessions, contributions and breaks? Note that you cannot undo this action.</p>"+
            "<h3>TAKE CARE:</h3> <strong>all FILES (material) attached to Contributions you have already uploaded, WILL BE DELETED TOO!!!.</strong>";
    new ConfirmPopup($T("Delete ALL entries from Timetable"), $T(txt), function(confirmed){
            if(confirmed){
                var confId = timetable["eventInfo"]["id"]
                var killProgress = IndicoUI.Dialogs.Util.progress($T("Deleting the entries..."));                
                indicoRequest('ictp_addons.deleteAllTimetable',
                        { confId: confId },
                          function(result, error){
                              if (!error) {
                                  killProgress();
                                  location.reload();
                              } else {
                                  killProgress();
                                  IndicoUtil.errorReport(error);
                              }
                            }
                    );
            }
        }).open();
};

function createTimetableProtectionDialog(timetable){
    new ChangeProtectionDialog(timetable).open();
};




type("ChangeProtectionDialog", ["ExclusivePopupWithButtons"], {

    /**
     * Draws the step 1: choose "starting time" or "duration" as action
     */
    __drawChooseAction: function(){
        var self = this;

        

        var setPublicRB = Html.radio({name:"changeprotectionAction", id:"protectionPublic", style:{verticalAlign: "middle"}});
        var setPublicLabel = Html.label({style: {fontWeight: "normal", paddingLeft: "5px"}},
                Html.div("setPublicLabelTitle", $T("Public")));
        setPublicLabel.dom.htmlFor = "setPublicRB";

        var setInheritingRB = Html.radio({name:"changeprotectionAction", id:"protectionInheriting", style:{verticalAlign: "middle"}});
        var setInheritingLabel = Html.label({style: {fontWeight: "normal", paddingLeft: "5px"}},
                Html.div("setInheritingLabelTitle", $T("Inheriting")));
        setInheritingLabel.dom.htmlFor = "setInheritingRB";

        var setRestrictRB = Html.radio({name:"changeprotectionAction", id:"protectionRestrict", style:{verticalAlign: "middle"}});
        var setRestrictLabel = Html.label({style: {fontWeight: "normal", paddingLeft: "5px"}},
                Html.div("setRestrictLabelTitle", $T("Restrict")));
        setRestrictLabel.dom.htmlFor = "setRestrictRB";




        var actionChoose = Html.table({cellpadding:0, cellPadding:0, cellspacing:0, cellSpacing:0});
        var actionChooseTitle = Html.div("changeprotectionTitle", $T("Choose the Protection Level"));
        var actionChooseTbody = Html.tbody();

        var publicTr = Html.tr();
        publicTr.append(Html.td("changeprotectionAction", setPublicRB));
        publicTr.append(Html.td({className: "changeprotectionAction", style:{paddingRight:pixels(5)}}, setPublicLabel));
        actionChooseTbody.append(publicTr);

        var inheritingTr = Html.tr();
        inheritingTr.append(Html.td("changeprotectionAction", setInheritingRB));
        inheritingTr.append(Html.td({className: "changeprotectionAction", style:{paddingRight:pixels(5)}}, setInheritingLabel));
        actionChooseTbody.append(inheritingTr);

        var restrictTr = Html.tr();
        restrictTr.append(Html.td("changeprotectionAction", setRestrictRB));
        restrictTr.append(Html.td({className: "changeprotectionAction", style:{paddingRight:pixels(5)}}, setRestrictLabel));
        actionChooseTbody.append(restrictTr);

        actionChoose.append(actionChooseTbody);



        setPublicRB.observeClick(function(){
                self.chooseprotectionButton.disabledButtonWithTooltip('enable');
                self.changeprotectionAction = "public";
        });
        setInheritingRB.observeClick(function(){
                self.chooseprotectionButton.disabledButtonWithTooltip('enable');
                self.changeprotectionAction = "inherit";
        });
        setRestrictRB.observeClick(function(){
                self.chooseprotectionButton.disabledButtonWithTooltip('enable');
                self.changeprotectionAction = "restrict";
        });

        return Html.div("chooseprotectionSection", actionChooseTitle, actionChoose);
    },






    _getButtons: function() {
        var self = this;
        return [
            [$T('Confirm'), function() {
            self.__setProtection();
            self.close();
            }],
            [$T('Cancel'), function() {
                self.close();
            }]
        ];
    },



    /**
     * Function called when the user presses the reschedule button
     */
    __setProtection: function() {
        var killProgress = IndicoUI.Dialogs.Util.progress($T("Setting Protection..."));                
        indicoRequest('ictp_addons.changeProtectionTimetable',
                { confId: this.confId, action: this.changeprotectionAction },
                  function(result, error){
                      if (!error) {
                          killProgress();
                          location.reload();
                      } else {
                          killProgress();
                          IndicoUtil.errorReport(error);
                      }
                    }
            );
    },
 


    /**
     * Draw the dialog
     */
    draw: function(){
        var self = this;

        this.chooseprotectionButton = this.buttons.eq(0);
        this.chooseprotectionButton.disabledButtonWithTooltip({
            tooltip: $T('Please select the protection level'),
            disabled: true
        });
        var actionChooseDiv = this.__drawChooseAction();

        this.mainContent = Html.div({style:{width:pixels(450)}}, actionChooseDiv);

        return this.ExclusivePopupWithButtons.prototype.draw.call(this, this.mainContent);


    }
},
    /**
     * Constructor
     */
    function(timetable){
        this.ExclusivePopupWithButtons($T('Set Protection for ALL Timetable entries'));
        this.confId = timetable["eventInfo"]["id"]
        this.changeprotectionAction = "noAction";
    }
);
